import java.io.*;

// Student class must implement Serializable
class Student implements Serializable {
    private static final long serialVersionUID = 1L;

    private String name;
    private int id;
    private String course;

    public Student(String name, int id, String course) {
        this.name = name;
        this.id = id;
        this.course = course;
    }

    public String toString() {
        return "Name: " + name + "\nID: " + id + "\nCourse: " + course;
    }

    public String getName() {
        return name;
    }
}

public class Main {
    public static void main(String[] args) {
        Student s1 = new Student("Hamza", 101, "Software Engineering");
        Student s2 = new Student("Ahmed", 102, "Electrical Engineering");

        // Display original students
        System.out.println("Original Student Objects:");
        System.out.println(s1);
        System.out.println(s2);

        // Serialize s1
        try (ObjectOutputStream oop = new ObjectOutputStream(new FileOutputStream("D:\\Coding\\Java\\" + s1.getName() + ".ser"))) {
            oop.writeObject(s1);
            System.out.println("\nSerialized " + s1.getName() + " to file.");
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Deserialize s1
        try (ObjectInputStream oip = new ObjectInputStream(new FileInputStream(s1.getName() + ".ser"))) {
            Student deserializedStudent = (Student) oip.readObject();
            System.out.println("\nDeserialized Student Object:");
            System.out.println(deserializedStudent);
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
        System.out.println("Current Working Directory: " + System.getProperty("user.dir"));

    }
}