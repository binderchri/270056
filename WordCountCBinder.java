//Needs java8
//javac WordCountCBinder.java
//java WordCountCBinder

import java.io.IOException;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.LinkOption;
import java.nio.file.Path;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class WordCountCBinder {
    public static void main(String[] args) throws IOException {
        String errorMsg = "Call program with: java WordCountCBinder -f <FileName> -ger|-eng";
        if(args.length < 3) {
            System.out.println(errorMsg);
            return;
        }

        String filename=null;
        String language=null;
        
        for(int i=0; i<args.length; i++) {
            String arg = args[i];
            if(arg.equals("-f") && (++i) < args.length) {
                filename = args[i];
                continue;
            }
        
            if(arg.equals("-ger"))
                language = "ger";
            else if (arg.equals("-eng"))
                language = "eng";
        }
        
        if(filename == null || language == null) {
            System.out.println(errorMsg);
            return;
        }
        
        Path path = FileSystems.getDefault().getPath(filename);

        if(Files.notExists(path, LinkOption.NOFOLLOW_LINKS)){
            System.out.println("Given input file must exist");
            return;
        }
        
        HashMap<String, Integer> map = new HashMap<String, Integer>();
        
        for (String line : Files.readAllLines(path)) {
            line = line.toLowerCase().replaceAll("'", "");
            
            if(language.equals("ger"))
                line = line.replaceAll("ö", "oe").replaceAll("ä", "ae").replaceAll("ü", "ue").replaceAll("ß", "ss");
            
            // http://stackoverflow.com/questions/1805518/replacing-all-non-alphanumeric-characters-with-empty-strings
            line = line.replaceAll("[^a-z0-9]", " ");
            
            for (String word : line.split(" ")) {
                if(word.length() == 0)
                    continue;
                
                int abundance = 0;
                if(map.containsKey(word))
                    abundance = map.get(word);
                
                map.put(word, abundance + 1);
            }    
        }
        
        // http://stackoverflow.com/a/23846961/2386941
        List<String> sortedWords = map.entrySet().stream()
                .sorted(Collections.reverseOrder(Map.Entry.comparingByValue()))
                .map(entry -> entry.getKey())
                .collect(Collectors.toList());
        
        String result = String.join(", ", sortedWords);

        System.out.println(result);
    }
}
