import java.util.*;
import twitter4j.*;
import twitter4j.conf.*;

class Test{

public static void main(String[] args){
	Test test = new Test();	
	test.go();
}

void go(){

    // The factory instance is re-useable and thread safe.
    Twitter twitter = TwitterFactory.getSingleton();
    try{
    List<Status> statuses = twitter.getUserTimeline("realDonaldTrump");
    
    System.out.println("Showing home timeline.");
    for (Status status : statuses) {
        System.out.println(status.getUser().getName() + ":" +
                           status.getText());
    }
    }catch(Exception ex){
	System.out.println("Ups.");
    }
}

}
