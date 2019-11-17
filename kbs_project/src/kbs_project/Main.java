package kbs_project;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;
import java.util.Stack;




/*
 * Projection Works
 * Join Works
 * Union Next
 * */
public class Main {
	
	public static int ColsTotal=0;
	public static int RowsTotal=0;
	
	public static HashMap<String, ArrayList<String>> Columns=null;
	
	public static String[][] Database= null;
	
	
	
	

	/*public static void Projection(HashMap<String,ArrayList<String>> Map, String[]columns){
		
		
		for(String keys:columns) {
			if(keys.contains("#")||keys.contains("%") ) {
				return;
			}else {
				System.out.print(keys + " , ");
			}
			
		}
		System.out.println();
		
		
		int k=0;
		boolean exit=true;
		while(true) {
			for(int i=0;i<columns.length;i++) {
				
				ArrayList<String> list= Map.get(columns[i]);
					
				
				
				if(k>list.size() /*&& k==columns.length-1*//*) { //-----> What if all the columns are not of equal size?
					exit=false;
					break;
						
				}else if( k<list.size() ){
						System.out.print(list.get(k)+ " , ");						
						
				}
				
			}
			System.out.println();
			k++;
			if(exit==false) {
				break;
			}
		}
			
	
			
			
		
		
		
		
		
		
		
	}*/
	
	
	public static void fillDatabase() {
        Database= new String[RowsTotal][ColsTotal + 1]; // 1 semantics
        int semanticsStart=ColsTotal;
		String fileName= "test.csv";
	    File file= new File(fileName);

	    // this gives you a 2-dimensional array of strings
	    Scanner inputStream;
        
	    try{
	        inputStream = new Scanner(file);

        	int index=0;
        	
	        while(inputStream.hasNext()){
	        	String line= inputStream.next();
	            String[] values = line.split(",");
	            
	            for(int i=0;i<values.length;i++) {
	            	Database[index][i]=values[i];
	            }
	            
	            
	            //Database[index]=values;
	            
	            if(index==0) {
	            	Database[index][semanticsStart++]="CTable";
	            	//Database[index][semanticsStart++]="Multiplicity";
	            	//Database[index][semanticsStart++]="Probability";
	            	//Database[index][semanticsStart++]="Certainity";
	            	//Database[index][semanticsStart++]="Polynomial";
	            	//Database[index][semanticsStart++]="Standard";
	            	semanticsStart=ColsTotal;
	            }else {
	            	Database[index][semanticsStart++]="P"+index;
	            	semanticsStart=ColsTotal;
	            }
	            
	            index++;
	            
	        } 
	        
	    }catch (FileNotFoundException e) {
	        e.printStackTrace();
	    }
	    
	    utility.print2Darray(Database);
	    
	}
	
	
	public static void scanDatabase(){
		String fileName= "test.csv";
	    File file= new File(fileName);

	    // this gives you a 2-dimensional array of strings
	    Scanner inputStream;
	    //String[] keys= null;
        
	    try{
	        inputStream = new Scanner(file);

        	int index=0;
        	//ArrayList<String> col= new ArrayList<String>();
        	
	        while(inputStream.hasNext()){
	            
	        	String line= inputStream.next();
	            String[] values = line.split(",");
	            //System.out.println("execute");
	            if(index==0){ // Get all the column names/ Attribute names


	            	/*index=values.length;
	            	
	            	ArrayList<String> check=null;
	            	
	            	Columns=new HashMap<String, ArrayList<String>>(index);// Attributes
	            	
	            	int in=0;

	            	for(String temp:values){
	            		Columns.put(temp, check);
	            		col.add(temp);
	            	}	
	            	keys=new String[Columns.size()];
	                for(String s:Columns.keySet()) {
	                	keys[in]=s;
	                	in++;
	                }*/
	            	// ColsTotal=Columns.size();
	            	ColsTotal=values.length;
	                
	               
	            	
	            }else{
	            	
	            	/*for(int i=0;i<values.length;i++){
	            		String val=values[i];
	            		String key=col.get(i);
	            		
	            		ArrayList<String> list= Columns.get(key);
	            		
	            		
	            		if(list==null) {
	            			list= new ArrayList<String>();
	            			list.add(val);
	            		}else {
	            			list.add(val);
	            		}
	            		
	            		
	            		Columns.put(key,list);
	            		
	            		
		            		
	            	}*/
	            }
	            RowsTotal++;
	            
	        }
	        inputStream.close();
	        
	        
	        //RowsTotal++;
	        
	        //System.out.println(" # Columns : "+ ColsTotal);
	        //System.out.println(" # Rows    : "+ RowsTotal);
	        
	        

	       // Projection(Columns,keys);
	        
	        
	        
	    }catch (FileNotFoundException e) {
	        e.printStackTrace();
	    }
	}
	
	
	/*public static void PrefixEvaluation(String substring) {
		
		System.out.println(substring );
		
		String values[]= substring.split(",");
		
		HashMap<String,ArrayList<String>>result=new HashMap<String, ArrayList<String>>(values.length);
		
		for(String key:values) {
			ArrayList<String> attributeList=Columns.get(key);
			result.put(key, attributeList);
			
		}
		
		//Projection(result, values);
		
		
		System.out.println();
		

	}*/

	
	/*public static void processQuery(String Query){
		
		
		
		char[] query = new char[Query.length()];
		query=Query.toCharArray();
		int index= 0;
		Stack<Character> stack= new Stack<Character>();
		System.out.println();
		while(index<query.length){
			stack.push(query[index]);
			
			if(query[index]==')'){
				String exp="", temp="";
				
				
				while(temp.compareTo("(")!=0){
					temp=stack.pop().toString();
					exp=temp+(String)exp;
				}
				
				exp=exp.substring(1, exp.length()-1);//---->remove the brackets and 
				
				
				
				
				PrefixEvaluation(exp);
				
				
				
				
				
				//exp=String.valueOf(infix(exp));
							
				stack.push('%');//-----> push the evaluated value in the stack
				
			}
			index++;
			
		}
		//check if number of opening brackets equals number of closing brackets
				int numOpenBracks=0;
				int numClosedBracks=0;			
				for(int i=0;i<query.length;i++)
				{
					if(query[i] == ')')
					{		
						numOpenBracks++;
					}
					if(query[i] =='(')
					{
						numClosedBracks++;
					}
				}
				if(numOpenBracks != numClosedBracks)
				{
					System.out.println("Syntax Error: Brackets");
				}						
				else
				{
					System.out.println(stack.pop() + " Last Else Condtion");
				}	
		
		
		
		
		
		
	}*/
	

	public static void tempQueryProcessing(String Query) {
		System.out.println(Query);
		
	}
	
	
	public static void main(String args[]) {
	
		scanDatabase();
		fillDatabase();
		
		String[] cols= {"A","B","CTable"};
		String[]cols2= {"B","C","CTable"};
		
		String[]cols3= {"A","C", "CTable"};
		String[]cols4= {"B","C", "CTable"};
		
		System.out.println("Projecting : A & B");
		String [][]temp = Operations.Projection(Database, cols, RowsTotal);
		utility.print2Darray(temp);
		
		System.out.println( "-------------- ");
		System.out.println("Projecting : B & C");
		String [][]temp2 = Operations.Projection(Database, cols2, RowsTotal);
		utility.print2Darray(temp2);
		System.out.println( "-------------- ");
		System.out.println("Joining : AB & BC");
		String [][]join12=Operations.Join(temp, temp2);
		utility.print2Darray(join12);
		
		String [][]temp3=Operations.Projection(Database, cols3, RowsTotal);
		utility.print2Darray(temp3);
		String [][]temp4=Operations.Projection(Database, cols4, RowsTotal);
		utility.print2Darray(temp4);
		System.out.println( " ----------------------------------- ");
		System.out.println("Joining : AC & BC");
		String [][]join34=Operations.Join(temp3, temp4);
		utility.print2Darray(join34);

		System.out.println( " ----------------------------------- ");
		/*System.out.println("Unioning the 2 Table");
		String[][]answer=Operations.Union(join12, join34);
		utility.print2Darray(answer);
		System.out.println( " ----------------------------------- ");*/

		
		//String[] order= {"A","C","CTable"};
		
		//String [][] answerProject=(Operations.Projection(answer, order, answer.length));
		
		//utility.print2Darray(answerProject);
		
		//System.out.println();


			
			
	}






	
	
}
