package kbs_project;
import java.util.ArrayList;
import java.util.HashMap;

public class utility {
	
	public static void printHashMap(HashMap<String, ArrayList<String>> Map) {
		for(String key:Map.keySet()){
			
			if(key.contains("#") || key.contains("%")) {
				break;
			}		
			System.out.print(key + " ");
			
			ArrayList<String> temp= new ArrayList<String>();
			temp=Map.get(key);
			
			for(String S:temp){
				System.out.print(S+" ");
			}
			System.out.println();
			
			}
	}
	
	public static void print2DarrayList(ArrayList<ArrayList<String>> Table) {
		for(int i=0;i<Table.size();i++) {
			for(int j=0;j<Table.get(i).size();j++) {
				System.out.print(Table.get(i).get(j) + " ");
			}
			System.out.println();
		}
	}
	
	public static void print2Darray(String[][]Table) {
		for(int i=0;i<Table.length;i++) {
	    	for(int j=0;j<Table[i].length;j++) {
	    		System.out.print(Table[i][j] + " , ");
	    	}
	    	System.out.println();
	    }
	}
	
	public static String[][] removeCommonColumn(String[][] Table) {
		
		String []Keys=Table[0];
		int prevIndex=0;
		for(int i=1;i<Keys.length;i++) {
			if(Keys[i].compareTo(Keys[prevIndex])==0) {
				break;
			}else {
				prevIndex++;
			}
		}
		
		String[][]TempTable= new String[Table.length][Table[0].length-1];
		
		int tempArrayIndex=0;
		
		for(int i=0;i<Table.length;i++) {
			String[]tempArray=new String[Table[0].length-1];
			for(int j=0;j<Table[i].length;j++) {
				if(j!=prevIndex) {
					tempArray[tempArrayIndex]=Table[i][j];
					tempArrayIndex++;
				}
					
			}
			tempArrayIndex=0;
			TempTable[i]=tempArray;
		}
		return TempTable;
	}
	
	public static String[] orderKeys(String[] Keys1, String[]Keys2) {
		return null;
	}
	
	public static boolean ifEqualTuples(String [] T1,String []T2) {
		
		for(int i=0;i<T1.length;i++) {
			if(T1[i].compareTo(T2[i])!=0){
				return false;
			}
		}
		return true;
	}
	
	public static int getLowerTuple(String []T1, String[]T2) {
		/*String temp1[]= new String[T1.length-1];
		String temp2[]= new String[T2.length-1];
		
		for(int i=0;i<temp1.length;i++) {
			temp1[i]=T1[i];
		}
		for(int j=0;j<temp2.length;j++) {
			temp2[j]=T2[j];
		}
		for(String s:temp1) {
			System.out.print(s + " ");
		}
		System.out.print ( "   ------   ");
		for(String s:temp2) {
			System.out.print(s + " ");
		}*/
		
		String CTable=(T1[T1.length-1] + " + "+T2[T2.length-1]);
		//System.out.println();
		System.out.println(CTable);

		
		for(int i=0;i<T1.length-1;i++) {//*******************************
			
			if(T1[i].compareTo(T2[i])<0) {
				return 1;
			}else if(T1[i].compareTo(T2[i])>0) {
				return 2;
			}
		}
		return 0;
	}
	
	public static String[][] removeCommonTuples(String[][]Table) {
		//System.out.println(" this code has reached");
		if(Table.length<=2) {
			return Table;
		}
		String[][]tempTable=new String[Table.length][Table[0].length];
		
		tempTable[0]=Table[0]; // Names of the Attributes/Column names + Ctable
		/*for(String s:tempTable[0]) {
			System.out.print(s + " . ");
		}*/
		
		/*System.out.println();*/
		
		tempTable[1]=Table[1]; // The 1st tuple is put in


		int valid=2; // 2 valid records the column names and the 1st tuple
		int insertion=2;
		for(int i=2;i<Table.length;i++) {
			String[] currentTuple=Table[i];
			String[] prevTuple=Table[i-1];
			
			int result=getLowerTuple(prevTuple, currentTuple);
			//System.out.println(result + " RESULTS");
			if(result!=0) {
				valid++;
				tempTable[insertion]=currentTuple;
				insertion++;
				
			}else {
				//update Semantics of prevTuple
				
				
			}
		}		
		//System.out.println(valid);
		
		String[][]finalTable=new String[valid][Table[0].length];
		for(int i=0;i<finalTable.length;i++) {
			finalTable[i]=tempTable[i];
		}

		
		
		return finalTable;
	}
	
 	public static String removeSpaces(String query) {
		return query.replaceAll("\\s+","");
	}

}
