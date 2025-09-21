
import java.io.FileWriter;
import java.io.IOException;



class Event{
    private String name, date, location;
    public Event(String name, String date, String location){
        this.name = name;
        this.date = date;
        this.location = location;
    }
    public String getName(){
        return name;
    }
    public String getDate(){
        return date;
    }
    public String getLocation(){
        return location;
    }
    public void conflictChecker(Event e){
        if(getDate() == e.getDate()){
            System.out.println("Event timing clashes with " + e.getName() +"!");
        }
        else{
            System.out.println("No event clash.");
        }
    }
}
class Seminar extends Event{
    private int noOfSpeakers;
    public Seminar(String name, String date, String location, int noOfSpeakers){
        super(name, date, location);
        this.noOfSpeakers = noOfSpeakers;
    }
    public void eventDetails(){
        System.out.println("---Seminar---\nName: " + getName() +"\nDate: " + getDate() + "\nLocation: " + getLocation()
        + "\nNumber of Speakers: " + noOfSpeakers);
    }
    public void fileHnadling(){
        try {
            FileWriter fw = new FileWriter(getName() + ".txt");
            fw.write("---Seminar---\nName: " + getName() +"\nDate: " + getDate() + "\nLocation: " + getLocation()
        + "\nNumber of Speakers: " + noOfSpeakers);
            System.out.println("File Saved!");
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }
}
class MusicalPerformance extends Event{
    private String performanceList;
    public MusicalPerformance(String name, String date, String location, String list){
        super(name, date, location);
        this.performanceList = list;
    }
    public void eventDetails(){
        System.out.println("---Concert---\nName: " + getName() +"\nDate: " + getDate() + "\nLocation: " + getLocation()
        + "\nPerformers: " + performanceList);
    }
    public void fileHnadling(){
        try {
            FileWriter fw = new FileWriter(getName() + ".txt");
            fw.write("---Concert---\nName: " + getName() +"\nDate: " + getDate() + "\nLocation: " + getLocation()
        + "\nPerformers: " + performanceList);
            System.out.println("File Saved!");
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }
}
public class Main{
    public static void main(String[] args) {
        Seminar sem = new Seminar("Speakers Session", "March 6", "SEECS", 7);
        MusicalPerformance mPerformance = new MusicalPerformance("Concert", "7 March", "SEECS", "Ali Zafar, Atif Aslam, Talha Anjum");
        Event e1 = new Event("Convocation", "March 6", "CIPS");
        Event e2 = new Event("Dinner", "March 8", "Mariot Hotel");
        sem.eventDetails();
        sem.conflictChecker(e1);
        System.out.println("\n\n\n");
        mPerformance.eventDetails();
        mPerformance.conflictChecker(e2);

        sem.fileHnadling();
        mPerformance.fileHnadling();
    }
}