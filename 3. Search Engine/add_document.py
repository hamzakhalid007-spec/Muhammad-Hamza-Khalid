from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import ujson as json
import os
import re
import time
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import logging

# Set up logging to keep track of what's happening
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Paths - these match your existing system structure
BASE_PATH = r"D:\Hamza\cord-19_2020-05-01"
LEXICON_PATH = os.path.join(BASE_PATH, "res", "lexicon", "cord19_lexicon.json")
FORWARD_INDEX_DIR = os.path.join(BASE_PATH, "res", "forward_indexing")
BACKWARD_INDEX_DIR = os.path.join(BASE_PATH, "res", "backward_indexing")
RAW_FILES_DIR = os.path.join(BASE_PATH, "2020-05-01", "all_files")

# Make sure the raw files directory exists
os.makedirs(RAW_FILES_DIR, exist_ok=True)


class QuickDocumentProcessor:
    """Handles rapid processing of a single document"""
    
    def __init__(self):
        # Load the existing lexicon once at startup for speed
        self.lexicon = self._load_lexicon()
        self.term_to_id = {term: info['term_id'] for term, info in self.lexicon.items()}
        self.next_term_id = max(info['term_id'] for info in self.lexicon.values()) + 1
        logger.info(f"Ready! Loaded {len(self.lexicon):,} existing terms")
    
    def _load_lexicon(self):
        """Load the current lexicon from disk"""
        try:
            with open(LEXICON_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Couldn't load lexicon: {e}")
            return {}
    
    def extract_text_from_json(self, data):
        """Pull out all the text from a paper JSON file"""
        text_parts = []
        
        # Grab the title if it's there
        if 'metadata' in data and 'title' in data['metadata']:
            title = data['metadata']['title']
            if title:
                text_parts.append(('title', str(title)))
        
        # Get the abstract
        if 'abstract' in data:
            if isinstance(data['abstract'], list):
                for item in data['abstract']:
                    if isinstance(item, dict) and 'text' in item:
                        text_parts.append(('abstract', str(item['text'])))
            elif isinstance(data['abstract'], str):
                text_parts.append(('abstract', data['abstract']))
        
        # Extract body text sections
        if 'body_text' in data and isinstance(data['body_text'], list):
            for idx, para in enumerate(data['body_text']):
                if isinstance(para, dict) and 'text' in para:
                    section_name = para.get('section', f'body_{idx}')
                    text_parts.append((section_name, str(para['text'])))
        
        # Don't forget the back matter
        if 'back_matter' in data and isinstance(data['back_matter'], list):
            for item in data['back_matter']:
                if isinstance(item, dict) and 'text' in item:
                    text_parts.append(('back_matter', str(item['text'])))
        
        return text_parts
    
    def tokenize_text(self, text):
        """Break text into individual words/terms that we care about"""
        # This regex finds words, including those with hyphens and numbers
        words = re.findall(r'\b[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9]\b|\b[A-Za-z]\b', text)
        
        tokens = []
        for position, word in enumerate(words):
            normalized = word.lower()  # lowercase for matching
            
            # Check if this term is already in our lexicon
            if normalized in self.term_to_id:
                tokens.append((normalized, position, word))
            elif word in self.term_to_id:  # check original case too (for abbreviations)
                tokens.append((word, position, word))
        
        return tokens
    
    def create_forward_index(self, doc_data, doc_id, source_type='custom'):
        """Build a forward index for this specific document"""
        start = time.time()
        
        # Extract all text sections from the document
        text_sections = self.extract_text_from_json(doc_data)
        
        if not text_sections:
            return None, "No text found in document"
        
        # Initialize the index structure
        forward_idx = {
            'document_id': doc_id,
            'source_type': source_type,
            'file_name': f"{doc_id}.json",
            'total_terms': 0,
            'unique_terms': 0,
            'sections': {},
            'term_frequencies': {},
            'metadata': {
                'indexed_at': datetime.now().isoformat(),
                'sections_count': len(text_sections)
            }
        }
        
        # Track terms across all sections
        all_tokens = []
        section_info = defaultdict(lambda: {'term_count': 0, 'char_length': 0, 'terms': defaultdict(int)})
        
        # Process each section
        for section_name, text in text_sections:
            tokens = self.tokenize_text(text)
            all_tokens.extend(tokens)
            
            section_info[section_name]['term_count'] += len(tokens)
            section_info[section_name]['char_length'] += len(text)
            
            for term, pos, original in tokens:
                section_info[section_name]['terms'][term] += 1
        
        # Calculate overall term frequencies
        term_freq = defaultdict(int)
        term_positions = defaultdict(list)
        
        for term, pos, original in all_tokens:
            term_freq[term] += 1
            term_positions[term].append(pos)
        
        forward_idx['total_terms'] = len(all_tokens)
        forward_idx['unique_terms'] = len(term_freq)
        
        # Store term data with lexicon IDs
        for term, freq in term_freq.items():
            term_id = self.term_to_id.get(term, -1)
            forward_idx['term_frequencies'][term] = {
                'term_id': term_id,
                'frequency': freq,
                'positions': term_positions[term][:100]  # keep first 100 positions
            }
        
        # Save section statistics
        for section, info in section_info.items():
            top_terms = dict(sorted(info['terms'].items(), key=lambda x: x[1], reverse=True)[:20])
            forward_idx['sections'][section] = {
                'term_count': info['term_count'],
                'char_length': info['char_length'],
                'top_terms': top_terms
            }
        
        elapsed = time.time() - start
        logger.info(f"Forward index created in {elapsed:.2f}s - {len(term_freq)} unique terms")
        
        return forward_idx, None
    
    def update_lexicon(self, forward_idx):
        """Add any new terms we found to the lexicon"""
        start = time.time()
        new_terms_added = 0
        
        term_frequencies = forward_idx.get('term_frequencies', {})
        
        for term, term_data in term_frequencies.items():
            freq = term_data.get('frequency', 0)
            
            if term in self.lexicon:
                # Term already exists - just update its frequency
                self.lexicon[term]['frequency'] += freq
            else:
                # Brand new term - add it to the lexicon
                self.lexicon[term] = {
                    'term_id': self.next_term_id,
                    'term': term,
                    'frequency': freq
                }
                self.term_to_id[term] = self.next_term_id
                self.next_term_id += 1
                new_terms_added += 1
        
        # Save the updated lexicon back to disk
        try:
            with open(LEXICON_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.lexicon, f, indent=2, ensure_ascii=False)
        except Exception as e:
            return f"Failed to save lexicon: {e}"
        
        elapsed = time.time() - start
        logger.info(f"Lexicon updated in {elapsed:.2f}s - {new_terms_added} new terms added")
        
        return None
    
    def save_forward_index(self, forward_idx, doc_id):
        """Save the forward index file"""
        output_dir = os.path.join(FORWARD_INDEX_DIR, 'custom_json')
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, f"{doc_id}.json")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(forward_idx, f, indent=2, ensure_ascii=False)
            logger.info(f"Forward index saved to {output_file}")
            return None
        except Exception as e:
            return f"Failed to save forward index: {e}"
    
    def get_prefix_bucket(self, term):
        """Figure out which 3-letter bucket this term belongs to"""
        term_lower = term.lower()
        
        # Handle terms that don't start with a letter
        if not term_lower or not term_lower[0].isalpha():
            return '000'
        
        # Get the first 3 characters, pad with underscores if needed
        prefix = term_lower[:3].ljust(3, '_')
        return prefix
    
    def update_backward_index(self, forward_idx, doc_id):
        """Update the inverted index buckets with this document's terms"""
        start = time.time()
        
        source_type = forward_idx.get('source_type', 'custom')
        term_frequencies = forward_idx.get('term_frequencies', {})
        
        # Group terms by their prefix buckets
        bucket_updates = defaultdict(dict)
        
        for term, term_data in term_frequencies.items():
            prefix = self.get_prefix_bucket(term)
            
            bucket_updates[prefix][term] = {
                'frequency': term_data.get('frequency', 0),
                'positions': term_data.get('positions', [])[:100],
                'source_type': source_type,
                'term_id': term_data.get('term_id', -1)
            }
        
        # Update each affected bucket file
        buckets_updated = 0
        for prefix, terms_to_add in bucket_updates.items():
            bucket_file = os.path.join(BACKWARD_INDEX_DIR, f"{prefix}.json")
            
            try:
                # Load existing bucket or create new one
                if os.path.exists(bucket_file):
                    with open(bucket_file, 'r', encoding='utf-8') as f:
                        bucket_data = json.load(f)
                else:
                    bucket_data = {
                        'prefix': prefix,
                        'term_count': 0,
                        'total_documents': 0,
                        'terms': {},
                        'created_at': datetime.now().isoformat()
                    }
                
                # Add or update terms in this bucket
                for term, term_info in terms_to_add.items():
                    if term not in bucket_data['terms']:
                        bucket_data['terms'][term] = {}
                        bucket_data['term_count'] += 1
                    
                    # Add this document to the term's posting list
                    bucket_data['terms'][term][doc_id] = term_info
                
                # Recalculate totals
                bucket_data['total_documents'] = sum(len(docs) for docs in bucket_data['terms'].values())
                
                # Save updated bucket
                with open(bucket_file, 'w', encoding='utf-8') as f:
                    json.dump(bucket_data, f, indent=2, ensure_ascii=False)
                
                buckets_updated += 1
                
            except Exception as e:
                logger.error(f"Failed to update bucket {prefix}: {e}")
                return f"Failed to update backward index bucket {prefix}: {e}"
        
        elapsed = time.time() - start
        logger.info(f"Backward index updated in {elapsed:.2f}s - {buckets_updated} buckets modified")
        
        return None
    
    def save_raw_document(self, doc_data, doc_id):
        """Save a copy of the original document to the raw files directory"""
        output_file = os.path.join(RAW_FILES_DIR, f"{doc_id}.json")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(doc_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Raw document saved to {output_file}")
            return None
        except Exception as e:
            return f"Failed to save raw document: {e}"
    
    def process_document(self, doc_data, doc_id):
        """Complete pipeline to add a document to the system"""
        total_start = time.time()
        logger.info(f"\n{'='*60}")
        logger.info(f"Starting to process document: {doc_id}")
        logger.info(f"{'='*60}")
        
        steps_completed = []
        
        try:
            # Step 1: Create forward index
            logger.info("Step 1/5: Building forward index...")
            forward_idx, error = self.create_forward_index(doc_data, doc_id)
            if error:
                return {'success': False, 'error': error, 'steps': steps_completed}
            steps_completed.append('forward_index')
            
            # Step 2: Update lexicon
            logger.info("Step 2/5: Updating lexicon...")
            error = self.update_lexicon(forward_idx)
            if error:
                return {'success': False, 'error': error, 'steps': steps_completed}
            steps_completed.append('lexicon')
            
            # Step 3: Save forward index
            logger.info("Step 3/5: Saving forward index...")
            error = self.save_forward_index(forward_idx, doc_id)
            if error:
                return {'success': False, 'error': error, 'steps': steps_completed}
            steps_completed.append('forward_index_saved')
            
            # Step 4: Update backward index
            logger.info("Step 4/5: Updating backward index...")
            error = self.update_backward_index(forward_idx, doc_id)
            if error:
                return {'success': False, 'error': error, 'steps': steps_completed}
            steps_completed.append('backward_index')
            
            # Step 5: Save raw document
            logger.info("Step 5/5: Saving raw document...")
            error = self.save_raw_document(doc_data, doc_id)
            if error:
                return {'success': False, 'error': error, 'steps': steps_completed}
            steps_completed.append('raw_saved')
            
            total_time = time.time() - total_start
            
            logger.info(f"\n{'='*60}")
            logger.info(f"SUCCESS! Document processed in {total_time:.2f} seconds")
            logger.info(f"Document ID: {doc_id}")
            logger.info(f"Unique terms: {forward_idx['unique_terms']}")
            logger.info(f"Total terms: {forward_idx['total_terms']}")
            logger.info(f"{'='*60}\n")
            
            return {
                'success': True,
                'doc_id': doc_id,
                'processing_time': round(total_time, 2),
                'stats': {
                    'unique_terms': forward_idx['unique_terms'],
                    'total_terms': forward_idx['total_terms'],
                    'sections': len(forward_idx['sections'])
                },
                'steps': steps_completed
            }
            
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e),
                'steps': steps_completed
            }


# Initialize the processor once when the server starts
processor = QuickDocumentProcessor()


# ============================================================================
# WEB INTERFACE
# ============================================================================

HTML_FRONTEND = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Document - CORD-19</title>
    <style>
        * { 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }
        
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
            padding: 40px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        h1 {
            color: #667eea;
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .subtitle {
            color: #718096;
            font-size: 16px;
        }
        
        .upload-area {
            border: 3px dashed #cbd5e0;
            border-radius: 12px;
            padding: 40px 20px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            margin-bottom: 20px;
        }
        
        .upload-area:hover {
            border-color: #667eea;
            background: #f7fafc;
        }
        
        .upload-area.dragover {
            border-color: #667eea;
            background: #edf2f7;
            transform: scale(1.02);
        }
        
        .upload-icon {
            font-size: 48px;
            color: #cbd5e0;
            margin-bottom: 16px;
        }
        
        .upload-text {
            color: #4a5568;
            font-size: 18px;
            font-weight: 500;
            margin-bottom: 8px;
        }
        
        .upload-hint {
            color: #a0aec0;
            font-size: 14px;
        }
        
        input[type="file"] {
            display: none;
        }
        
        .file-info {
            background: #f7fafc;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 20px;
            display: none;
        }
        
        .file-info.active {
            display: block;
        }
        
        .file-name {
            color: #2d3748;
            font-weight: 600;
            margin-bottom: 4px;
            word-break: break-all;
        }
        
        .file-size {
            color: #718096;
            font-size: 14px;
        }
        
        .doc-id-section {
            margin-bottom: 20px;
        }
        
        .doc-id-section label {
            display: block;
            color: #4a5568;
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 14px;
        }
        
        .doc-id-section input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.2s;
        }
        
        .doc-id-section input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn-process {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: none;
        }
        
        .btn-process.active {
            display: block;
        }
        
        .btn-process:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        
        .btn-process:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .progress-section {
            display: none;
            margin-top: 20px;
        }
        
        .progress-section.active {
            display: block;
        }
        
        .progress-bar {
            height: 8px;
            background: #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 16px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s ease;
        }
        
        .progress-steps {
            list-style: none;
        }
        
        .progress-step {
            padding: 8px 0;
            color: #a0aec0;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .progress-step.completed {
            color: #48bb78;
        }
        
        .progress-step.active {
            color: #667eea;
            font-weight: 600;
        }
        
        .step-icon {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            border: 2px solid currentColor;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
        }
        
        .result-section {
            display: none;
            margin-top: 20px;
            padding: 20px;
            border-radius: 8px;
        }
        
        .result-section.active {
            display: block;
        }
        
        .result-section.success {
            background: #f0fdf4;
            border: 2px solid #86efac;
        }
        
        .result-section.error {
            background: #fef2f2;
            border: 2px solid #fca5a5;
        }
        
        .result-title {
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 12px;
        }
        
        .result-section.success .result-title {
            color: #16a34a;
        }
        
        .result-section.error .result-title {
            color: #dc2626;
        }
        
        .result-stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-top: 16px;
        }
        
        .stat-box {
            background: white;
            padding: 12px;
            border-radius: 6px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: 700;
            color: #667eea;
        }
        
        .stat-label {
            font-size: 12px;
            color: #718096;
            margin-top: 4px;
        }
        
        .btn-reset {
            margin-top: 16px;
            width: 100%;
            padding: 12px;
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .btn-reset:hover {
            background: #667eea;
            color: white;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .spinner {
            display: inline-block;
            width: 16px;
            height: 16px;
            border: 2px solid currentColor;
            border-top-color: transparent;
            border-radius: 50%;
            animation: spin 0.6s linear infinite;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📄 Add New Document</h1>
            <p class="subtitle">Upload a research paper to the CORD-19 index</p>
        </div>
        
        <div class="upload-area" id="uploadArea">
            <div class="upload-icon">📁</div>
            <div class="upload-text">Click to browse or drag & drop</div>
            <div class="upload-hint">JSON files only</div>
            <input type="file" id="fileInput" accept=".json">
        </div>
        
        <div class="file-info" id="fileInfo">
            <div class="file-name" id="fileName"></div>
            <div class="file-size" id="fileSize"></div>
        </div>
        
        <div class="doc-id-section">
            <label for="docId">Document ID (optional)</label>
            <input type="text" id="docId" placeholder="Leave empty for auto-generated ID">
        </div>
        
        <button class="btn-process" id="btnProcess">
            Process Document
        </button>
        
        <div class="progress-section" id="progressSection">
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            <ul class="progress-steps">
                <li class="progress-step" id="step1">
                    <span class="step-icon">1</span>
                    <span>Building forward index</span>
                </li>
                <li class="progress-step" id="step2">
                    <span class="step-icon">2</span>
                    <span>Updating lexicon</span>
                </li>
                <li class="progress-step" id="step3">
                    <span class="step-icon">3</span>
                    <span>Saving forward index</span>
                </li>
                <li class="progress-step" id="step4">
                    <span class="step-icon">4</span>
                    <span>Updating backward index</span>
                </li>
                <li class="progress-step" id="step5">
                    <span class="step-icon">5</span>
                    <span>Saving raw document</span>
                </li>
            </ul>
        </div>
        
        <div class="result-section" id="resultSection">
            <div class="result-title" id="resultTitle"></div>
            <div id="resultMessage"></div>
            <div class="result-stats" id="resultStats"></div>
            <button class="btn-reset" onclick="resetForm()">Add Another Document</button>
        </div>
    </div>
    
    <script>
        let selectedFile = null;
        let fileData = null;
        
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        const btnProcess = document.getElementById('btnProcess');
        const docIdInput = document.getElementById('docId');
        const progressSection = document.getElementById('progressSection');
        const progressFill = document.getElementById('progressFill');
        const resultSection = document.getElementById('resultSection');
        const resultTitle = document.getElementById('resultTitle');
        const resultMessage = document.getElementById('resultMessage');
        const resultStats = document.getElementById('resultStats');
        
        // Click to upload
        uploadArea.addEventListener('click', () => fileInput.click());
        
        // Drag and drop handlers
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFile(files[0]);
            }
        });
        
        // File input change
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFile(e.target.files[0]);
            }
        });
        
        // Handle selected file
        function handleFile(file) {
            if (!file.name.endsWith('.json')) {
                alert('Please select a JSON file');
                return;
            }
            
            selectedFile = file;
            fileName.textContent = file.name;
            fileSize.textContent = formatFileSize(file.size);
            fileInfo.classList.add('active');
            btnProcess.classList.add('active');
            
            // Auto-generate doc ID from filename if not provided
            if (!docIdInput.value) {
                const autoId = file.name.replace('.json', '').replace(/[^a-zA-Z0-9_-]/g, '_');
                docIdInput.value = autoId;
            }
            
            // Read file content
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    fileData = JSON.parse(e.target.result);
                } catch (err) {
                    alert('Invalid JSON file');
                    resetForm();
                }
            };
            reader.readAsText(file);
        }
        
        // Format file size
        function formatFileSize(bytes) {
            if (bytes < 1024) return bytes + ' B';
            if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
            return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
        }
        
        // Process document
        btnProcess.addEventListener('click', async () => {
            if (!fileData) {
                alert('Please wait for the file to load');
                return;
            }
            
            const docId = docIdInput.value.trim() || `doc_${Date.now()}`;
            
            // Show progress
            btnProcess.disabled = true;
            progressSection.classList.add('active');
            resultSection.classList.remove('active');
            
            try {
                const response = await fetch('/add', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        doc_data: fileData,
                        doc_id: docId
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showSuccess(result);
                } else {
                    showError(result);
                }
                
            } catch (err) {
                showError({ error: err.message });
            }
        });
        
        // Show success result
        function showSuccess(result) {
            // Mark all steps as completed
            for (let i = 1; i <= 5; i++) {
                document.getElementById(`step${i}`).classList.add('completed');
            }
            progressFill.style.width = '100%';
            
            // Show result
            resultSection.classList.add('active', 'success');
            resultSection.classList.remove('error');
            resultTitle.textContent = '✅ Document Added Successfully!';
            resultMessage.innerHTML = `
                <p style="color: #15803d; margin-bottom: 8px;">
                    Document <strong>${result.doc_id}</strong> has been processed and added to the system.
                </p>
                <p style="color: #15803d; font-size: 14px;">
                    Processing completed in ${result.processing_time} seconds
                </p>
            `;
            
            // Show stats
            resultStats.innerHTML = `
                <div class="stat-box">
                    <div class="stat-value">${result.stats.unique_terms}</div>
                    <div class="stat-label">Unique Terms</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">${result.stats.total_terms}</div>
                    <div class="stat-label">Total Terms</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">${result.stats.sections}</div>
                    <div class="stat-label">Sections</div>
                </div>
            `;
        }
        
        // Show error result
        function showError(result) {
            // Mark failed step
            const steps = result.steps || [];
            const stepMap = {
                'forward_index': 1,
                'lexicon': 2,
                'forward_index_saved': 3,
                'backward_index': 4,
                'raw_saved': 5
            };
            
            steps.forEach(step => {
                const stepNum = stepMap[step];
                if (stepNum) {
                    document.getElementById(`step${stepNum}`).classList.add('completed');
                }
            });
            
            progressFill.style.width = `${(steps.length / 5) * 100}%`;
            
            // Show error
            resultSection.classList.add('active', 'error');
            resultSection.classList.remove('success');
            resultTitle.textContent = '❌ Processing Failed';
            resultMessage.innerHTML = `
                <p style="color: #b91c1c;">
                    ${result.error || 'An unknown error occurred'}
                </p>
            `;
            resultStats.innerHTML = '';
        }
        
        // Reset form
        function resetForm() {
            selectedFile = null;
            fileData = null;
            fileInput.value = '';
            docIdInput.value = '';
            fileInfo.classList.remove('active');
            btnProcess.classList.remove('active');
            btnProcess.disabled = false;
            progressSection.classList.remove('active');
            resultSection.classList.remove('active');
            progressFill.style.width = '0%';
            
            // Reset all steps
            for (let i = 1; i <= 5; i++) {
                const step = document.getElementById(`step${i}`);
                step.classList.remove('completed', 'active');
            }
        }
    </script>
</body>
</html>
"""


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/', methods=['GET'])
def home():
    """Serve the add document interface"""
    return Response(HTML_FRONTEND, mimetype='text/html')


@app.route('/add', methods=['POST', 'OPTIONS'])
def add_document():
    """Handle document addition"""
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    try:
        data = request.get_json()
        doc_data = data.get('doc_data')
        doc_id = data.get('doc_id', f'custom_{int(time.time())}')
        
        if not doc_data:
            return jsonify({'success': False, 'error': 'No document data provided'}), 400
        
        # Process the document
        result = processor.process_document(doc_data, doc_id)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in add_document endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'steps': []
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'CORD-19 Document Addition Service',
        'lexicon_terms': len(processor.lexicon)
    }), 200


if __name__ == '__main__':
    print("\n" + "="*60)
    print("CORD-19 Document Addition Service")
    print("="*60)
    print("Server: http://localhost:8082")
    print("Open this in your browser to add documents")
    print("="*60 + "\n")
    
    try:
        from waitress import serve
        print("Using Waitress server\n")
        serve(app, host='0.0.0.0', port=8082, threads=2)
    except ImportError:
        print("Using Flask dev server\n")
        app.run(host='0.0.0.0', port=8082, debug=False, threaded=True)