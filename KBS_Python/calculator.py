def queryProcessing(query, Semantics):
    '''
        {#[] ( {U { J [{#[]()}]  ({#[]()}) }  ({ J [{#()[]}] ({#()[]}) } } ) }
    '''


    #q=" {#[] (      { U [{ J [{#[]()}]  ({#[]()}) }] ({ J [{#[]()}] ({#[]()}) })  }    ) }"

    q="{ #[A,C]( {U[{ J [ { #[A,B](R) } ] ( { #[B,C](R) } ) }] ( { J [ { #[A,C](R) } ] ( {#[B,C](R) } ) })} )  } "

    q=q.replace(" ","")

    print(q)
    exit=False
    res=1

    while q.__contains__('{'):
        index=0
        forwardBrackIndex = []
        for i in q:
            if q[index]=='{':
                forwardBrackIndex.append(index)
            elif q[index]=='}':
                startBrack=forwardBrackIndex.pop()
                exp=q[startBrack: index+1]
                front=q[0:startBrack]
                back=q[index+1:]
                TABLENAME="Table"+str(res)
                newQ=front+TABLENAME+back
                res=res+1
                q=newQ
                print(exp) #Send exp to the process based on what the 2nd character is
                print(q)
                break

            index=index+1

    print("Query Completed ")

queryProcessing("","hello")
