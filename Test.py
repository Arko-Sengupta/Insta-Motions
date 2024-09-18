from backend.SentimentAnalyzer import AnalyzeData

if __name__=="__main__":
    
    username = 'aniketsahu_02'
    password = 'Ani02@'
    
    Obj = AnalyzeData()
    df, bool = Obj.run(username, password)
    
    print(df, bool)