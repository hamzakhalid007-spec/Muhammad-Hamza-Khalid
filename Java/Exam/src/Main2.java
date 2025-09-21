
interface Event{
    public void eventManagement();
}
class Seminar implements Event{
    private String name, date, location;
    private int noOfSpeakers;
    public Seminar(String name, String date, String location, int noOfSpeakers){
        this.name = name;
        this.date = date;
        this.location = location;
        this.noOfSpeakers = noOfSpeakers;
    }
    @Override
    public void eventManagement()  {
        System.out.println("Event managed by Mr. Hamza And Mr. Rafay.");
    }
    public void eventDetails(){
        System.out.println("---Seminar---\nName: " + name +"\nDate: " + date + "\nLocation: " + location
        + "\nNumber of Speakers: " + noOfSpeakers);
    }
}
class MusicalPerformance implements Event{
    private String name, date, location, list;
    public MusicalPerformance(String name, String date, String location, String list){
        this.name = name;
        this.date = date;
        this.location = location;
        this.list = list;
    }
    @Override
    public void eventManagement() {
        System.out.println("Event managed by SE 15-B.");
    }
    public void eventDetails(){
        System.out.println("---Concert---\nName: " + name +"\nDate: " + date + "\nLocation: " + location
        + "\nPerformers: " + list);
    }
}
public class Main2 {
    public static void main(String[] args){
        Seminar sem1 = new Seminar("Speakers Session", "March 6", "CIPS", 7);
        MusicalPerformance mPerformance1 = new MusicalPerformance("Concert", "7 March", "SEECS", "Ali Zafar, Atif Aslam, Talha Anjum");

        sem1.eventDetails();
        sem1.eventManagement();
        System.out.println("\n\n\n");
        mPerformance1.eventDetails();
        mPerformance1.eventManagement();
    }
}
