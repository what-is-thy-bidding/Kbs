package kbs_project;
import java.util.Arrays;


public class Operations {
	
	public static String[][] Projection(String [][]Table ,  
										String []Order, 
										int Rows) {
		//System.out.println("Printing in the projection function");
		
		
		int[] colIndex=new int[Order.length];// gets all the column indexes of the required Columns

		//System.out.println( " T1 "+ Order.length + " "+Table[0].length);
		
		for(int j=0;j<Order.length;j++) {
			String Key=Order[j];
			for(int i=0;i<Table[0].length;i++) {
				String col=Table[0][i];
				if(col.compareTo(Key)==0) {
					colIndex[j]=i;
					break;
				}
			}
			if(colIndex[j]==-1) {
				System.out.println("Column doesn't exists");
				return null;
			}
		}
			
		
		String[][]column= new String[Rows][Order.length];
		
		for(int j=0;j<colIndex.length;j++) {
			int index=colIndex[j];
			for(int i=0;i<Rows;i++) {
				column[i][j]=Table[i][index];
			}
		}
		
		//utility.print2Darray(column);
		
		String[][]finalResult =utility.removeCommonTuples(column);
		
		return finalResult;
		
	}

	public static String[][] Join(String[][]Table1, String[][]Table2) {
		
		Table1=Projection(Table1, Table1[0], Table1.length);
		//System.out.println("Table 1");
		//utility.print2Darray(Table1);
		Table2=Projection(Table2,Table2[0],Table2.length);
		//System.out.println("Table 2");
		//utility.print2Darray(Table2);
		
		String semantics= Table1[0][Table1[0].length-1];
		String T1Semantics[]= new String[Table1.length];
		String T2Semantics[]= new String[Table2.length];
		
		for(int i=0;i<Table1.length;i++) {
			T1Semantics[i]=Table1[i][Table1[i].length-1];
		}
		for(int i=0;i<Table2.length;i++) {
			T2Semantics[i]=Table2[i][Table2[i].length-1];
		}
		


		// Find all the common join Column
		int T1Index=-1;
		int T2Index=-1;
		boolean exit=false;
		for(int i=0;i<Table1[0].length;i++) {
			T1Index=i;
			String T1=Table1[0][i];
			
			for(int j=0;j<Table2[0].length;j++) {
				String T2=Table2[0][j];
				if(T1.compareTo(T2)==0) {
					T2Index=j;
					exit=true;
					break;
				}
				
			}
			if(exit) {// ----> In case the tables have more than 1 column in common
				break;
			}
		}
		
		if(T2Index==-1) {
			System.out.println("Cannot Join Tables");
			return null;
		}
		
		//System.out.println("Joining tables at: "+Table1[0][T1Index] );
		//System.out.println("Table 1 Index = "+ T1Index);
		//System.out.println("Table 2 Index = "+ T2Index);
		//System.out.println("----------");
		
		/*
		 * Switch values1[T1Index] = values[values1.length-1]------> Bringing the common join value
		 * 		  values1[values.length-1]=values1[T1Index]			 to the last of the 1st Table
		 * 
		 * Switch values2[T2Index] = values[values2.length-1]------> Bringing the common join value
		 * 		  values2[values2.length-1]=values2[T1Index]		 to the front of the 2nd Table
		 * 
		 * */

		String values1[]=new String[Table1[0].length];
		System.arraycopy(Table1[0], 0, values1, 0, Table1[0].length);

		String values2[]=new String[Table2[0].length];
		System.arraycopy(Table2[0], 0, values2, 0, Table2[0].length);
		
		/*String []newOrder1=new String[values1.length];
		String []newOrder2=new String[values2.length];
		
		for(int i=0;i<values1.length;i++) {
			newOrder1[i]=values1[i];
			
		}
		for(int i=0;i<values2.length;i++) {
			newOrder2[i]=values2[i];
			
		}*/
		
		// Switch T1Index and put it at the end of newOrder1
		// Switch T2Index and put it at the front of newOrder2
		
		/*String temp= newOrder1[T1Index];
		newOrder1[T1Index]=newOrder1[values1.length-1];
		newOrder1[values1.length-1]=temp;
		
		
		temp= newOrder2[T2Index];
		newOrder2[T2Index]=newOrder2[0];
		newOrder2[0]=temp;*/
		
		int T1Rows=Table1.length-1,T2Rows=Table2.length-1;//Excluding the 1st ROW

		
		//Table1=Projection(Table1, newOrder1, T1Rows+1);

		
		//Table2=Projection(Table2, newOrder2, T2Rows+1);

		String [][] ComputationTable=
			new String[(T1Rows*T2Rows)+1][(values1.length-1+values2.length-1)+1];

		//int length=newOrder1.length+newOrder2.length;
		
		int length=(values1.length-1)+(values2.length-1);

		/*for(int i=0;i<newOrder1.length;i++) {
			ComputationTable[0][i]=newOrder1[i];
			length--;
		}*/
		for(int i=0;i<values1.length-1;i++) {
			ComputationTable[0][i]=values1[i];
			length--;
		}
		for(int i=0;i<values2.length-1;i++) {
			ComputationTable[0][length]=values2[i];
			length++;
		}

		ComputationTable[0][length]=semantics;
		//1st row of Computation Table A B B C CTABLE
		
		//utility.print2Darray(ComputationTable);
		
		int computationIndex=1;
		
		//System.out.println(" ----++++++-------");

		for(int i=1;i<Table1.length;i++) {
			for(int j=1;j<Table2.length;j++) {
				String [] T1= new String[Table1[i].length-1];
				System.arraycopy(Table1[i], 0, T1, 0, Table1[i].length-1);	
				/*for(String T:T1) {
					System.out.print(T + " - ");
				}*/

				String [] T2=new String[Table2[j].length-1];
				System.arraycopy(Table2[j], 0, T2, 0, Table2.length-2);
				/*for(String T:T2) {
					System.out.print(T + " - ");
				}*/

				if(T1[T1Index].compareTo(T2[T2Index])==0) {
					// Filling the computation Table

					String[]combined= new String[T2.length+T1.length+1];
					
					System.arraycopy(T1, 0, combined, 0,T1.length);
					System.arraycopy(T2, 0, combined, T1.length, T2.length);
					
					ComputationTable[computationIndex]=combined;
					String Semantics="("+T1Semantics[i]+" * " +T2Semantics[j]+")";
					
					//System.out.println(Semantics);
					
					ComputationTable[computationIndex][ComputationTable[0].length-1]=Semantics;
					computationIndex++;
				}else {
					//System.out.println();
				}

				
			}


			
		}
		//System.out.println(" ----++++++-------");
		//utility.print2Darray(ComputationTable);


		String[][]finalTable=new String[computationIndex][];
		/**/int in=0;
		
		
		for(String[]array:ComputationTable) {
			
			if(in<finalTable.length) {
				
				finalTable[in++]=array;
			
			}else {
				break;
			}
		}
		
		
		String[][]testTable= utility.removeCommonColumn(finalTable);
		
		//System.out.println("testTable Table");
		//utility.print2Darray(testTable);
		//System.out.println(" **** ");
		return testTable;
		
	}

	public static String[][] Union(String[][]Table1,String[][]Table2){
		/*
		 * First check if these tables can be unionized
		 * */		
		if(Table1[0].length!=Table2[0].length) {
			System.out.println("The tables cannot be unioned");
			return null;
		}
		/*System.out.println(" ------------ ");
		utility.print2Darray(Table1);
		System.out.println(" ------------ ");
		utility.print2Darray(Table2);*/
		
		String[]Attributes1= new String[Table1[0].length];
		String[]Attributes2= new String[Table2[0].length];

		String[]Semantics1=new String[Table1.length];
		
		//System.out.print("Semantics 1 ");
		for(int i=0;i<Semantics1.length;i++) {
			String tuple=Table1[i][Table1[i].length-1];
			Semantics1[i]=tuple;
			//System.out.println(tuple + " *************");
		}
		//System.out.println(" ------------------------------------ ");
		String[]Semantics2=new String[Table2.length];
		
		//System.out.print("Semantics 2 ");
		for(int i=0;i<Semantics2.length;i++) {
			String tuple=Table2[i][Table2[i].length-1];
			Semantics2[i]=tuple;
			//System.out.println(tuple + " *************");
		}
		for(int i=0;i<Table1[0].length;i++) {
			Attributes1[i]=Table1[0][i];
			Attributes2[i]=Table2[0][i];
		}
		
		
		
		
		Arrays.sort(Attributes1);

		Arrays.sort(Attributes2);

		
		
		for(int i=0;i<Attributes1.length;i++) {
			if(Attributes1[i].compareTo(Attributes2[i])!=0) {
				System.out.println("Tables Cannot be unionized "+Attributes1[i] 
								  +" != "+Attributes2[i]);
				return null;
			}
		}
		
		Table1=Projection(Table1,Attributes1,Table1.length);
		//utility.print2Darray(Table1);

		Table2=Projection(Table2,Attributes2,Table2.length);
		//utility.print2Darray(Table2);
		
		String ComputationTable[][]= new String[Table1.length+Table2.length-1][Attributes1.length+1];
		
		int T1Index=1, T2Index=1;
		int insertion=1;
		//ComputationTable has to have more than 1 length
		ComputationTable[0]=Table1[0]; //Inputing all the attributes name/Column names
		int valid=1;
		while(insertion <ComputationTable.length) {
			//System.out.println(T1Index + " "+ T2Index+ " "+ insertion);
			//If the records are equal, pick 1 and increment both
			if(T1Index<Table1.length && T2Index<Table2.length) {
				String [] tuple1=Table1[T1Index];
				String [] tuple2=Table2[T2Index];
				
				// 0 -> if both are equal
				// 1 -> if tuple1 should be inserted first
				// 2 -> if tuple2 should be inserted first
				int result=utility.getLowerTuple(tuple1, tuple2);
				
				if(result==0) {
					//T1Index && T2Index cTables
					String CTable=tuple1[tuple1.length-1]+" + "+ tuple2[tuple2.length-1];
					tuple1[tuple1.length-1]=CTable;
					ComputationTable[insertion]= tuple1;
					T1Index++;
					T2Index++;
					valid++;
				}else if(result==1){
					ComputationTable[insertion]=tuple1;
					T1Index++;
					valid++;
				}else if(result==2) {
					ComputationTable[insertion]=tuple2;
					T2Index++;
					valid++;
				}
				
			}else if(T1Index<Table1.length ) {
				String[] tuple= Table1[T1Index];
				ComputationTable[insertion]=tuple;
				T1Index++;
				valid++;
			}else if(T2Index<Table2.length) {
				String[]tuple=Table2[T1Index];
				ComputationTable[insertion]=tuple;
				T2Index++;
				valid++;
			}
			insertion++;

		}
		
		
		String[][]finalTable=new String[valid][];
		
		for(int i=0;i<finalTable.length;i++) {
			finalTable[i]=ComputationTable[i];
			
		}
		
		
		
		
		/*System.out.println("Tables Can Be unionized ");
		
		System.out.println();
		System.out.println();*/

		//utility.print2Darray(finalTable);
		
		
		return finalTable;
	}

	
	
}
