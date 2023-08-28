import pandas as pd
import time
import webbrowser
import datetime
import sqlite3 as db
import os
import pickle
# VARIBLES LOCAL-----------------------------
STD_PATH='C:\\Users\\lenovo\Documents\\vs\\inventory_management\\app\\res\\'
# STD_PATH='.\\res\\'s
# 
def check_start_new():
    if os.path.isfile(STD_PATH+'master.db') and os.path.isfile(STD_PATH+'master') and os.path.isfile(STD_PATH+'udf'):
        return False
    else:
        return True
def get_matching_list(word,type):
    # it sends data back to web in the form of array []
    # two argument type-string,word-word to be matched,type-pl/description
    word=word.upper()
    try:
        udf = pd.read_pickle(STD_PATH+'udf')
    except:
        udf = pd.DataFrame({'date':[],'pl': [], 'description': [],
                            's_ns': [], 'unit': [], 'rate': [],'to_be_display':[]})
        udf.to_pickle(STD_PATH+'udf')
    if type == 'pl_number_input':
        from_match_list= udf['pl'].to_list()
    else:
        from_match_list= udf['description'].to_list()
    # sentence_to_display=udf['to_be_display'].to_list()
    # new=pd.DataFrame([{'percentage':22,'pl':'ritik','sentence':'removed','to_display':'this'}])
    # new=new[new['sentence']!='removed']
    word=word.split()
    flag=0
    p=[]
    for k,i in enumerate(from_match_list):
        flag=1
        no_of_matching = 0
        for j in word:
            if j in i.upper():
                no_of_matching=no_of_matching+1
            else:
                pass
        if len(word)==0:
            return []
        percentage=(no_of_matching/len(word))*100
        p.append(percentage)
        # df2=pd.DataFrame([{'percentage':percentage,'sentence':i,'to_display':sentence_to_display[k]}])

        # new=pd.concat([new,df2],ignore_index=True)
    udf['percentage']=p
    if flag==0:
        return []
    new=udf.sort_values(by='percentage',ascending=False)
    new=new[new['percentage']>50]
    if new.shape[0]>10:
        new_d=new['to_be_display'].to_list()[:10]
        pl_new=new['pl'].to_list()[:10]
    # new=new[10:]
    else:
        new_d=new['to_be_display'].to_list()
        pl_new=new['pl'].to_list()
    return [new_d,pl_new]

def login(data):
    if data['username']=='RITIK RAUSHAN' and data['password']=='123456789':
        store_gen(True,'LOGIN')
        return {'action':'success'}
    else:
        return {'action':'fail'}
def direct_function(name_function,data):
    if name_function=='login':

        return login(data)
    if name_function == 'autocomplete_setup':
        return autocomplete_setup(data)
    elif name_function == 'submit':
        return submit(data)
    elif name_function=='udf_manager':
        return udf_manager(data=data)
    elif name_function=='last20_issue':
        return last20_issue()
    elif name_function=='last20_recieve':
        return last20_recieve()
    elif name_function=='update':
        return update(data)
    elif name_function=='delete':
        return delete(data)
    elif name_function=='master_filter':
        return master_filter(data)
    elif name_function=="pl_card":
        return pl_card(data)
    elif name_function=='get_template_list':
        return get_template()
    elif name_function=='create_template':
        return create_template(data)
    elif name_function=='delete_template':
       return  delete_template(data)
    elif name_function=='blank_format':
        return blank_template(data)
    elif name_function=='filled_template':
        return filled_template(data)
    elif name_function=='filled_data_template':
        return filled_data_template(data)
    elif name_function=='get_udf_delete':
        return get_udf_delete()
    elif name_function=='delete_udf':
        return delete_udf(data)
    elif name_function=='eac_template':
        return eac_template()
    elif name_function=='set_eac':
        return set_eac()
    elif name_function=='balance_template':
       return balance_template()
    elif name_function=='set_balance':
       return set_balance()
    elif name_function=='lm_set':
        return lm_set(data)
    elif name_function=='s_l_20_issue':
        return s_l_20_issue()
    elif name_function=='s_l_20_recieve':
        return s_l_20_recieve()
    elif name_function=='last_10_loco':
        return last_10_loco()
    elif name_function=='latest_items_recieved':
        return latest_items_recieved()
    elif name_function=='critical_item':
        return critical_item()
    elif name_function=='inactive_items':
        return inactive_items()
    elif name_function=='show_balance':
        return show_balance()
    else:
        pass
def show_balance():
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    df=pd.DataFrame({'date':[],'pl':[],'description':[],'stock':[]})
    udf=pd.read_pickle(STD_PATH+'udf')
    udf.set_index('pl',inplace=True)
    today=datetime.datetime.now().date()
    date=today.strftime("%Y-%m-%d")
    for i in udf.index:
        df.loc[len(df.index)]=[date,i,udf.loc[i,'description'],balance(i)]
    df=convert_to_str(df)
    col=df.columns.to_list()
    row=df.index.to_list()
    filename=STD_PATH+'show_balance.csv'
    df.to_csv(filename)
    data={'editable':'no','close':'no','delete_btn':'no','filename':filename
          ,'des_to_display':'STOCK POSITION','export_to_csv':'yes','df':df.to_dict(orient='index'),
          'fit_content':'yes','position':'none','editable_column':['date','qty','remark'],'row':row,'column':col}
    return {'action':'success','data':data}
def inactive_items():
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    today=datetime.datetime.now()
    df=pd.DataFrame({'date':[],'pl':[],'description':[],'stock':[]})
    udf=pd.read_pickle(STD_PATH+'udf')
    udf.set_index('pl',inplace=True)
    master_db=db.connect(STD_PATH+'master.db')
    cur=master_db.cursor()
    for i in udf.index:
        res=cur.execute("SELECT MAX(date_ordinal) FROM master WHERE pl="+db_str(i))
        res=res.fetchall()
        date=res[0][0]
        if date==None:
            df.loc[len(df.index)]=['not_found',i,udf.loc[i,'description'],balance(i)]
        else:
            date=res[0][0]
            date=datetime.datetime.fromordinal(date)
            delta=today-date
            day=delta.days
            if day>95:
                date=date.strftime("%Y-%m-%d")
                df.loc[len(df.index)]=[date,i,udf.loc[i,'description'],balance(i)]
            else:
                pass
    df=convert_to_str(df)
    col=df.columns.to_list()
    row=df.index.to_list()
    filename=STD_PATH+'inactive.csv'
    df.to_csv(filename)
    data={'editable':'no','close':'no','delete_btn':'no','filename':filename
          ,'des_to_display':'inactive item','export_to_csv':'yes','df':df.to_dict(orient='index'),
          'fit_content':'yes','position':'none','editable_column':['date','qty','remark'],'row':row,'column':col}
    return {'action':'success','data':data}

def critical_item():
    try:
        eac=pd.read_pickle(STD_PATH+'eac')
    except:
        return {'action':'failed','message':'eac file not found'}
    eac.set_index('pl',inplace=True)
    udf=pd.read_pickle(STD_PATH+'udf')
    df=pd.DataFrame({'pl':[],'description':[],'stock':[],'EAC':[]})
    udf.set_index('pl',inplace=True)
    for i in udf.index:
        try:
            ea_c=eac.loc[i,'eac']
            bal=balance(i)
            if bal<(ea_c/4):
                df.loc[len(df.index)]=[i,udf.loc[i,'description'],bal,ea_c]
        except:
            df.loc[len(df.index)]=[i,udf.loc[i,'description'],'eac not found','not_found']
    
    df=convert_to_str(df)
    col=df.columns.to_list()
    row=df.index.to_list()
    filename=STD_PATH+'critical.csv'
    df.to_csv(filename)
    data={'editable':'no','close':'no','delete_btn':'no','filename':filename
          ,'des_to_display':'Critical item','export_to_csv':'yes','df':df.to_dict(orient='index'),
          'fit_content':'yes','position':'none','editable_column':['date','qty','remark'],'row':row,'column':col}
    return {'action':'success','data':data}
def balance(pl):
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    master_db=db.connect(STD_PATH+'master.db')
    cur=master_db.cursor()
    res=cur.execute("SELECT SUM(qty) FROM master WHERE i_r_flag='issue' AND pl="+db_str(pl))
    res=res.fetchall()
    issue=res[0][0]
    if issue==None:
        issue=0
    else:
        issue=res[0][0]
    res=cur.execute("SELECT SUM(qty) FROM master WHERE i_r_flag='recieve' AND pl="+db_str(pl))
    res=res.fetchall()
    recieve=res[0][0]
    if recieve==None:
        recieve=0
    else:
        recieve=res[0][0]
    try:
        open=pd.read_pickle(STD_PATH+'open_balance')
        open.set_index('pl',inplace=True)
        open=open.loc[pl,'open']
    except:
        open=0
    return open+recieve-issue
def latest_items_recieved():
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    udf=pd.read_pickle(STD_PATH+'udf')
    udf=udf.sort_values(by='date',ascending=True)
    s=udf[udf['s_ns']=='stock']
    s=s[-5:]
    ns=udf[udf['s_ns']=='non stock']
    ns=ns[-5:]
    cp=udf[udf['s_ns']=='cash purchase']
    cp=cp[-5:]
    rn=udf[udf['s_ns']=='r note']
    rn=rn[-5:]
    df=pd.concat([s,ns,cp,rn])
    date=[]
    for i in df['date']:
        x=datetime.datetime.fromordinal(i)
        date.append(x.strftime("%Y-%m-%d"))
    df['date']=date
    df=df[['date','pl','description','s_ns','unit','rate']]
    df=convert_to_str(df)
    col=df.columns.to_list()
    row=df.index.to_list()
    filename=STD_PATH+'last_10_loco.csv'
    df.to_csv(filename)
    data={'editable':'no','close':'no','delete_btn':'no','filename':filename
          ,'des_to_display':'LATEST ENTERED NEW ITEMS','export_to_csv':'yes','df':df.to_dict(orient='index'),
          'fit_content':'yes','position':'none','editable_column':['date','qty','remark'],'row':row,'column':col}
    return {'action':'success','data':data}
def last_10_loco():
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    df=get_loco_list()
    df=convert_to_str(df)
    
    if df.shape[0]<=0:
        return {'action':'empty','message':''}
    
    df=df[-10:]
    filename=STD_PATH+'last_10_loco.csv'
    df.to_csv(filename)
    col=df.columns.to_list()
    row=df.index.to_list()
    data={'editable':'no','close':'no','delete_btn':'no','filename':filename
          ,'des_to_display':'LAST 10 LOCO','export_to_csv':'yes','df':df.to_dict(orient='index'),
          'fit_content':'yes','position':'none','editable_column':['date','qty','remark'],'row':row,'column':col}
    return {'action':'success','data':data}
def s_l_20_recieve():
    # get 20 recieve from master df and return pl, description, qty
        # get 20 issue from master df and return pl, description, qty
    try:
        master = pd.read_pickle(STD_PATH+'master')
    except:
        master = pd.DataFrame({'ucode': [], 'timestamp': [], 'date': [],'date_ordinal':[],'pl': [], 'description': [],
                               'qty': [], 's_ns': [], 'unit': [],  'issued_to': [],
                               'loco_number': [], 'rate': [], 'remark': [], 'issue_check': []})
        master.to_pickle(STD_PATH+'master')
    master=master[master['issue_check']=='recieve']
    master=master[-20:]
    master.set_index('ucode', inplace=True)
    master = master[['date', 'pl','description', 'qty','s_ns','unit','rate','remark']]
    # master['date']=master['date'].apply(lambda x: x.strftime("%d-%m-%y"))
    master=convert_to_str(master)
    filename=STD_PATH+'s_l_20_recieved.csv'
    master.to_csv(filename)
    if master.shape[0]<=0:
        return {'action':'empty'}
    col=master.columns.to_list()
    row=master.index.to_list()
    data={'editable':'no','close':'no','delete_btn':'no','filename':filename
          ,'des_to_display':'last 20 entry in recieve','export_to_csv':'yes','df':master.to_dict(orient='index'),
          'fit_content':'yes','position':'none','editable_column':['date','qty','remark'],'row':row,'column':col}
    return {'action':'success','data':data}
def s_l_20_issue():
    # get 20 issue from master df and return pl, description, qty
    try:
        master = pd.read_pickle(STD_PATH+'master')
    except:
        master = pd.DataFrame({'ucode': [], 'timestamp': [], 'date': [],'date_ordinal':[],'pl': [], 'description': [],
                               'qty': [], 's_ns': [], 'unit': [],  'issued_to': [],
                               'loco_number': [], 'rate': [], 'remark': [], 'issue_check': []})
        master.to_pickle(STD_PATH+'master')
    master=master[master['issue_check']=='issue']
    master=master[-20:]
    master.set_index('ucode', inplace=True)
    master = master[['date', 'pl','description', 'qty','s_ns','unit','issued_to','loco_number','rate','remark']]
    master=convert_to_str(master)
    file_name=STD_PATH+'s_l_20_issue.csv'
    master.to_csv(file_name)
    if master.shape[0]<=0:
        return {'action':'empty'}
    col=master.columns.to_list()
    row=master.index.to_list()
    data={'editable':'no','close':'no','delete_btn':'no','filename':file_name
          ,'des_to_display':'last 20 entry in issue','export_to_csv':'yes','df':master.to_dict(orient='index'),
          'fit_content':'yes','position':'none','editable_column':['date','qty','remark'],'row':row,'column':col}
    return {'action':'success','data':data}
def lm_set(data):
    data=data.split('.')
    if len(data)!=3:
        return {'action':'failed','message':'invalid lm'}
    store_gen(data[0],'section_name')
    try:
        data=int(data[-1])
    except:
        return {'action':'failed','message':'invalid lm'}
    store_gen(int(data),'lm_last')
    return {'action':'success'}
def set_balance():
    path=STD_PATH+'temp.csv'
    try:
        df=pd.read_csv(path)
    except:
        return {'action':'failure','message':'check file may be corrupt'}
    df_col=list(df.columns)
    if 'pl' in df_col and 'description' in df_col and 'OPENING BALANCE' in df_col:
        pass
    else:
        return {'action':'failed','message':'pl or description column not found'}
    pl=list(map(lambda x:str(x),df['pl'].to_list()))
    df['pl']=pl
    description=df['description'].to_list()
    udf=pd.read_pickle(STD_PATH+'udf')
    for i in df['pl']:
        if i in udf['pl'].to_list():
            pass
        else:
            return {'action':'failed','message':'check file format'}
    for i in udf['pl']:
        if i in df['pl'].to_list():
            pass
        else:
            return {'action':'failed','message':'check file format'}
    open=[]
    for i in df.index:
        pl=df.loc[i,'pl']
        op=df.loc[i,'OPENING BALANCE']
        a_bal=balance(pl)
        if pl in udf['pl'].to_list():
            try:
                op=float(op)
                if op>a_bal:
                    open.append(op-a_bal)
                else:
                    open.append(a_bal-op)
            except:
                return {'action':'failed','message':'some error occured at pl:'+pl}
        else:
            return {'action':'failed','message':'some error in template'}
    df['open']=open
    df=df[['pl','open']]
    df.to_pickle(STD_PATH+'open_balance')
    return {'action':'success','message':''}
def balance_template():
    try:
        udf=pd.read_pickle(STD_PATH+'udf')
    except:
        return
    udf=pd.read_pickle(STD_PATH+'udf')
    udf=udf[[ 'pl', 'description','s_ns', 'unit', 'rate']]
    x=[]
    for i in udf.index:
        x.append('')
    udf['OPENING BALANCE']=x
    filename=STD_PATH+'balance.csv'
    udf.to_csv(filename)
    return {'action':'success','filename':filename}

def set_eac():
    path=STD_PATH+'temp.csv'
    try:
        df=pd.read_csv(path)
    except:
        return {'action':'failure','message':'check file may be corrupt'}
    df_col=list(df.columns)
    if 'pl' in df_col and 'description' in df_col and 'EAC' in df_col:
        pass
    else:
        return {'action':'failed','message':'pl or description column not found'}
    # pl=df['pl'].to_list()
    # description=df['description'].to_list()
    udf=pd.read_pickle(STD_PATH+'udf')
    eac=[]
    df['pl']=list(map(lambda x:str(x),df['pl'].to_list()))
    for i in df['pl']:
        if i in udf['pl'].to_list():
            pass
        else:
            return {'action':'failed','message':'check file format'}
    for i in udf['pl']:
        if i in df['pl'].to_list():
            pass
        else:
            return {'action':'failed','message':'check file format'}
    for i in df.index:
        pl=str(df.loc[i,'pl'])
        ea=df.loc[i,'EAC']
        if pl in udf['pl'].to_list():
            try:
                eac.append(float(ea))
            except:
                return {'action':'failed','message':'some error occured at pl:'+pl}
        else:
            return {'action':'failed','message':'some error in template'}
    df['eac']=eac
    
    df=df[['pl','eac']]
    df.to_pickle(STD_PATH+'eac')

    return {'action':'success','message':''}

def eac_template():
    try:
        udf=pd.read_pickle(STD_PATH+'udf')
    except:
        return
    udf=pd.read_pickle(STD_PATH+'udf')
    udf=udf[[ 'pl', 'description','s_ns', 'unit', 'rate']]
    x=[]
    for i in udf.index:
        x.append('')
    udf['EAC']=x
    filename=STD_PATH+'eac_template.csv'
    udf.to_csv(filename)
    return {'action':'success','filename':filename}
def get_udf_delete():
    try:
        udf=pd.read_pickle(STD_PATH+'udf')
    except:
        return 
    # udf = pd.DataFrame({'date': [], 'pl': [], 'description': [],
                            # 's_ns': [], 'unit': [], 'rate': [], 'to_be_display': []})
    udf=udf[[ 'pl', 'description','s_ns', 'unit', 'rate']]
    pl=udf['pl'].to_list()
    udf['pli']=pl
    udf.set_index('pli',inplace=True)
    udf=convert_to_str(udf)
    file_name=STD_PATH+'udf_temp.csv'
    udf.to_csv(file_name)
    col=udf.columns.to_list()
    row=udf.index.to_list()
    data={'editable':'yes','close':'yes','delete_btn':'yes','filename':file_name
          ,'des_to_display':'','export_to_csv':'yes','df':udf.to_dict(orient='index'),
          'fit_content':'yes','position':'absolute','editable_column':['description', 'unit', 'rate'],'row':row,'column':col}
    return {'action':'success','data':data}
def delete_udf(data):
    pl=data['ucode']
    udf=udf=pd.read_pickle(STD_PATH+'udf')
    udf=udf[udf['pl']!=pl]
    udf.to_pickle(STD_PATH+'udf')
    return {'action':'success','data':''}
def submit(data):
    # this function recieve data from web when submit button is clicked
    # format of data rcieved
    # {'date':date,'pl':pl number,'description':description,''
    # }
    # all value in dic form,and value are in string format
    # this function create std dict and std data according to dat type and store it in master dataframe whict store
    # 100 row and in master.db file
    # last lm dict
    try:
        master = pd.read_pickle(STD_PATH+'master')
    except:
        master = pd.DataFrame({'ucode': [], 'timestamp': [], 'date': [],'date_ordinal':[],'pl': [], 'description': [],
                               'qty': [], 's_ns': [], 'unit': [], 'issued_to': [],
                               'loco_number': [], 'rate': [], 'remark': [], 'issue_check': []})
        master.to_pickle(STD_PATH+'master')
        # checked means it alread returned through function and user is syaing yes this time
    # afetr getting data match pl,description ,s_ns,unit with udf
    # if not found or mismatch return action:failed, message to display
    udf = pd.read_pickle(STD_PATH+'udf')
    try:
        ucode = master[-1:]['ucode'].to_list()[0] + 1
    except:
        # first time making entry
        ucode=1
    timestamp = datetime.datetime.now().timestamp()
    date_str = data['date'] #'2023-02-22' is format returned from js
    date=datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    date_str=str(date.strftime('%d-%m-%Y'))
    date_ordinal=date.toordinal()
    qty = float(data['qty']).__round__(2)
    s_ns = data['s_ns']
    i_r_flag = data['i_r_flag']
    pl=data['pl']
    description = data['description']
    unit = data['unit']
    rate = float(data['rate'])

    if pl in udf['pl'].to_list():
        temp_df=udf[udf['pl']==pl]
        desc_c=temp_df['description'].to_list()[0]
        unit_c = temp_df['unit'].to_list()[0]
        s_ns_c = temp_df['s_ns'].to_list()[0]
        if desc_c==description and unit_c==unit and s_ns_c==s_ns:
            udf.loc[temp_df.index[0],'rate']=rate
            pass
        else:
            message=''
            if desc_c!=description:
                message+='descritpion not match to std description kindly check description\n'
            elif unit_c==unit:
                message+='unit not match to std unit kindly check unit\n'
            else:
                message+='stock non stock selection not match to std stock non stock kindly check unit\n'
            return {'action':'failed','message':message}
    else:
        if description in udf['description'].to_list():
            temp_df = udf[udf['description'] == description]
            pl_c = temp_df['pl'].to_list()[0]
            unit_c = temp_df['unit'].to_list()[0]
            s_ns_c = temp_df['s_ns'].to_list()[0]
            if pl_c == pl and unit_c == unit and s_ns_c == s_ns:
                udf.loc[temp_df.index[0], 'rate'] = rate
                pass
            else:
                message = ''
                if pl_c != pl:
                    message += 'pl not match to std pl kindly check pl\n'
                elif unit_c == unit:
                    message += 'unit not match to std unit kindly check unit\n'
                else:
                    message += 'stock non stock selection not match to std stock non stock kindly check unit\n'
                return {'action': 'failed', 'message': message}


        else:
            return {'action':'failed','message':'both pl and description not matching kindly check'}
            pass
            # this section check for duplicate entry
    duplicate = master[master['pl'] == pl]
    duplicate = duplicate[duplicate['date'] == date_str]
    if duplicate.shape[0] > 0:
        if duplicate['qty'].to_list()[0] == qty and data['duplicate'] != 'checked':
            message=duplicate[['date','pl','description','qty']].to_dict(orient='index')
            return {'action': 'duplicate', 'message': str(message)}
        else:
            pass
    else:
        pass

    # lm format is E3 AUX.2023.01
    # if i_r_flag == 'recieve':
    #     if s_ns == 'stock' or s_ns == 'non stock':
    #         try:
    #             lm_last=get_gen('lm_last')
    #         except:
    #             lm_last=1
    #             store_gen(lm_last,'lm_last')
    #         lm= get_gen('section_name')+'.' + str(datetime.datetime.now().year) + '.' + str(int(lm_last))
    #         master_last_lm=master[master['lm']==lm]

    #         if master_last_lm.shape[0] < 4:
    #             lm = get_gen('section_name')+'.' + str(datetime.datetime.now().year) + '.' + str(int(lm_last))
                
    #         else:
    #             lm = get_gen('section_name')+'.' + str(datetime.datetime.now().year) + '.' + str(int(lm_last) + 1)
    #             lm_last+=1
    #     else:
    #         lm = ''
    # else:
    #     lm = ''
    if i_r_flag == 'recieve':
        issued_to = ''
        loco_number = ''
    else:
        pass

    if i_r_flag == 'issue':
        issued_to = data['issued_to']
        if issued_to == 'loco':
            loco_number = data['loco_number']
        else:
            loco_number = ''

    remark = data['remark']

    data_to_stored = [ucode, timestamp, date_str,date_ordinal, pl, description, qty, s_ns, unit,
                       issued_to, loco_number, rate, remark, i_r_flag]

    master.loc[ucode] = data_to_stored

    master=master[-3000:]
    master.to_pickle(STD_PATH+'master')
    udf.to_pickle(STD_PATH+'udf')
    if os.path.isfile(STD_PATH+'master.db'):
        pass
    else:
        masterdb = db.connect(STD_PATH+'master.db')
        cur = masterdb.cursor()
        cur.execute("""CREATE TABLE master(ucode, timestamp, date,date_ordinal, pl, description, qty, s_ns, unit,
                               issued_to, loco_number, rate, remark, i_r_flag)""")
        masterdb.commit()
        masterdb.close()

    masterdb=db.connect(STD_PATH+'master.db')
    data_to_stored = (ucode, timestamp, date_str, date_ordinal, pl, description, qty, s_ns, unit,
                     issued_to, loco_number, rate, remark, i_r_flag)
    cur = masterdb.cursor()
    cur.execute("INSERT INTO master VALUES "+str(data_to_stored))
    # res = cur.execute("SELECT ucode FROM master ")
    # print(res.fetchall())
    masterdb.commit()
    # res = cur.execute("SELECT ucode FROM master ")
    # print(res.fetchall())
    masterdb.close()
    return {'action': 'success', 'data': ''}

def autocomplete_setup(data):
    # this function recieve data in jason string format and
    # it returns value of unique list value based on incoming data
    try:
        udf = pd.read_pickle(STD_PATH+'udf')
    except:
        udf = pd.DataFrame({'pl': [], 'description': [],
                            's_ns': [], 'unit': [], 'rate': []})
        udf.to_pickle(STD_PATH+'udf')
    # data structure will be like
    # {'data_type':'descripiton/pl','data':'data'}
    # alla value are string
    value = udf[udf['pl']== data['data']]
    if value.shape[0] == 0:
        return {'status': 'new',
                'data': ''}
    if value.shape[0] > 0:
        if value.shape[0] > 1:
            udf.drop_duplicates(subset=['pl'], keep='last', inplace=True)
            udf.drop_duplicates(subset=['description'], keep='last', inplace=True)
            udf.to_pickle(r'\py_res\udf')
        return {'status': 'ok',
                'data': {
                    'pl': value['pl'].to_list()[0],
                    'description': value['description'].to_list()[0],
                    's_ns': value['s_ns'].to_list()[0],
                    'unit': value['unit'].to_list()[0],
                    'rate': value['rate'].to_list()[0]
                }}

    else:
        return {'status': 'fail', 'data': ''}
def udf_manager(data):
    try:
        udf = pd.read_pickle(STD_PATH+'udf')
    except:
        udf = pd.DataFrame({'date': [], 'pl': [], 'description': [],
                            's_ns': [], 'unit': [], 'rate': [], 'to_be_display': []})
        udf.to_pickle(STD_PATH+'udf')
    unit = data['unit']
    s_ns = data['s_ns']
    o_s_f=True
    if s_ns=='stock':
        pl = data['pl']
    else:
        if data['pl'] in udf['pl'].to_list():
            pl = data['pl']
            o_s_f=False
        elif s_ns=='non stock':
            if data['pl'] in udf['pl'].to_list():
                pl = data['pl']
            try:
                last_pl_ns=get_gen('last_pl_ns')
                pl='NS'+str(int(last_pl_ns[2:])+1)
            except:
                pl='NS100001'
                store_gen(pl,'last_pl_ns')
        elif s_ns=='cash purchase':
            try:
                last_pl_cp=get_gen('last_pl_cp')
                pl='CP'+str(int(last_pl_cp[2:])+1)
            except:
                pl='CP100001'
                store_gen(pl,'last_pl_cp')
        else:
            # R note
            try:
                last_pl_rn=get_gen('last_pl_rn')
                pl='RN'+str(int(last_pl_rn[2:])+1)
            except:
                pl='RN100001'
                store_gen(pl,'last_pl_rn')
        
    descritpion = data['description']
    rate = float(data['rate']).__round__(2)
    date = datetime.datetime.now().date().toordinal()
    to_be_display = str(pl) + ':' + descritpion
    if data['action']=='store':
        if pl in udf['pl'].to_list():
            return {'action':'failed',"message":'data already present as '+str(udf[udf['pl']==pl].to_dict(orient='records'))}
        # if descritpion in udf['description'].to_list():
        #     return {'action':'failed',"message":'data already present as '+str(udf[udf['description']==descritpion].to_dict(orient='records'))}
        else:
            pass
        # udf = pd.DataFrame({'pl': [], 'description': [],
        #                     's_ns': [], 'unit': [], 'rate': [], 'to_be_display': []})
        try:
            index=udf.index[-1]
        except:
            index=1
        udf.loc[index+1] = [date,pl,descritpion,s_ns,unit,rate,to_be_display]
        if o_s_f:
            if s_ns=='non stock':
                try:
                    store_gen(pl,'last_pl_ns')
                except:
                    pass
                
            elif s_ns=='cash purchase':
                try:
                    store_gen(pl,'last_pl_cp')
                except:
                    pass
                    
            elif s_ns=='R note':
            # R note
                try:
                    store_gen(pl,'last_pl_rn')
                except:
                    pass
            else:
                pass
        udf.to_pickle(STD_PATH+'udf')
        return {'action':'success'}
    elif data['action']=='update':
        duplicate=udf[udf['pl']==pl]
        if duplicate.shape[0]==0:
            duplicate=udf[udf['description']==descritpion]
            if duplicate.shape[0]==0:
                return{'action':'failed','message':'check description and pl'}
        udf.loc[duplicate.index[0]]=[date,pl,descritpion,s_ns,unit,rate,to_be_display]
        udf.to_pickle(STD_PATH+'udf')
        return {'action':'updated'}
    else:
        return {'action':'incorrect response'}

def pl_card(data):
    # to be display, ucode,(pl,description),date,open,recieve,issue,close,loco,other shed,rate,s_ns,unit,lm,etc
    # input-pl,description,date
    try:
        udf = pd.read_pickle(STD_PATH+'udf')
    except:
        udf = pd.DataFrame({'date': [], 'pl': [], 'description': [],
                            's_ns': [], 'unit': [], 'rate': [], 'to_be_display': []})
        udf.to_pickle(STD_PATH+'udf')
    pl=data['pl']

    if pl in udf['pl'].to_list():
        pass
    else:
        return {'action':'failed','message':'check pl'}
    where={}
    where['pl=']=pl
    description = data['description']
    # if description in udf['description'].to_list():
    #     pass
    # else:
    #     return {'action': 'failed', 'message': 'check description'}

    date_from=data['date_from']
    if date_from=='':
        try:
            date_from=get_gen('date_from')
            date_from=datetime.datetime.strptime(date_from, '%Y-%m-%d').date().toordinal()
        except:
            date_from='2023-01-01'
            store_gen(date_from,'date_from')
            date_from=datetime.datetime.strptime(date_from, '%Y-%m-%d').date().toordinal()
    else:
    
        date_from=datetime.datetime.strptime(date_from, '%Y-%m-%d').date().toordinal() # small date
        # where['date_ordinal>=']=date_from
    date_to=data['date_to']
    if date_to=='':
        date_to=datetime.datetime.now().date().toordinal()
    else:
        date_to=datetime.datetime.strptime(date_to, '%Y-%m-%d').date().toordinal() # large date
        # where['date_ordinal<=']=date_to
    if date_to<=date_from or date_to>datetime.datetime.now().date().toordinal():
        return {'action':'failed','message':'check date'}
    st='SELECT * FROM master WHERE '
    for i,j in where.items():
        st=st+' '+i+''+db_str(j)+' AND'

    st=st[:-3]
    st=st+';'
    masterdb=db.connect(STD_PATH+'master.db')
    cur=masterdb.cursor()
    res=cur.execute(st)
    res=res.fetchall()
    masterdb.close()
    df = pd.DataFrame({'ucode': [], 'timestamp': [], 'date': [], 'date_ordinal': [], 'pl': [], 'description': [],
                           'qty': [], 's_ns': [], 'unit': [], 'issued_to': [],
                           'loco_number': [], 'rate': [], 'remark': [], 'issue_check': []})
    for i in res:
        df.loc[len(df.index)]=list(i)
    df.set_index('ucode',inplace=True)
    # HERE SET OPENING BALANCE OF STOCK
    df.sort_values(by='date_ordinal', ascending=True,inplace=True)
    
    if df.shape[0]<=0:
        return {'action':'empty','message':'no data found'}
    try:
        opendf=pd.read_pickle(STD_PATH+'open_balance')
        opendf.set_index('pl',inplace=True)
        open_balance=float(opendf.loc[pl,'open'])
    except:
        open_balance=0
    open=[]
    recieved=[]
    close=[]
    closing_balance=open_balance
    issue=[]
    for i in df.index:
        qty=df['qty'][i]
        if df['issue_check'][i]=='recieve':
            open_balance=closing_balance
            open.append(open_balance)
            recieved.append(qty)
            issue.append(0)
            closing_balance = open_balance + qty
            close.append(closing_balance)
        else:
            open_balance=closing_balance
            open.append(open_balance)
            recieved.append(0)
            issue.append(qty)
            closing_balance = open_balance - qty
            close.append(closing_balance)
    df['open_balance']=open
    df['recieved']=recieved
    df['issue']=issue
    df['closing_balance']=close
    df=df[df['date_ordinal']>=date_from]
    df=df[df['date_ordinal']<=date_to]
    df=df[['date','open_balance','recieved','issue','closing_balance','issued_to','loco_number','rate','remark']]
    df=convert_to_str(df)
    filename=STD_PATH+'pl_card.csv'
    df.to_csv(filename)
    col=df.columns.to_list()
    row=df.index.to_list()
    udf=udf[udf['pl']==pl]
    
    display='PL-'+str(pl)+'       Description:'+description+'      Type:'+udf['s_ns'].to_list()[0]+'    Unit:'+udf['unit'].to_list()[0]+'    Rate:'+str(udf['rate'].to_list()[0])
    data={'editable':'no','close':'yes','delete_btn':'no','filename':filename
          ,'des_to_display':display,'export_to_csv':'yes','df':df.to_dict(orient='index'),
          'fit_content':'yes','position':'absolute','editable_column':[],'row':row,'column':col}
    return {'action':'success','data':data}
def last20_issue():
    # get 20 issue from master df and return pl, description, qty
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    try:
        master = pd.read_pickle(STD_PATH+'master')
    except:
        master = pd.DataFrame({'ucode': [], 'timestamp': [], 'date': [],'date_ordinal':[],'pl': [], 'description': [],
                               'qty': [], 's_ns': [], 'unit': [], 'issued_to': [],
                               'loco_number': [], 'rate': [], 'remark': [], 'issue_check': []})
        master.to_pickle(STD_PATH+'master')
    master=master[master['issue_check']=='issue']
    master=master[-20:]
    master.set_index('ucode', inplace=True)
    master = master[['date', 'pl','description', 'qty','s_ns','unit','issued_to','loco_number','rate','remark']]
    master=convert_to_str(master)
    file_name=STD_PATH+'last_20_issued.csv'
    master.to_csv(STD_PATH+'last_20_issued.csv')
    if master.shape[0]<=0:
        return {'action':'empty'}
    col=master.columns.to_list()
    row=master.index.to_list()
    if get_gen('LOGIN'):
        editable='yes'
        delete_btn='yes'
    else:
        editable='no'
        delete_btn='no'
    data={'editable':editable,'close':'no','delete_btn':delete_btn,'filename':file_name
          ,'des_to_display':'last 20 entry in issue','export_to_csv':'yes','df':master.to_dict(orient='index'),
          'fit_content':'yes','position':'none','editable_column':['date','qty','remark'],'row':row,'column':col}
    return {'action':'success','data':data}
def last20_recieve():
    # get 20 recieve from master df and return pl, description, qty
        # get 20 issue from master df and return pl, description, qty
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    try:
        master = pd.read_pickle(STD_PATH+'master')
    except:
        master = pd.DataFrame({'ucode': [], 'timestamp': [], 'date': [],'date_ordinal':[],'pl': [], 'description': [],
                               'qty': [], 's_ns': [], 'unit': [],'issued_to': [],
                               'loco_number': [], 'rate': [], 'remark': [], 'issue_check': []})
        master.to_pickle(STD_PATH+'master')
    master=master[master['issue_check']=='recieve']
    master=master[-20:]
    master.set_index('ucode', inplace=True)
    master = master[['date', 'pl','description', 'qty','s_ns','unit','rate','remark']]
    master=convert_to_str(master)
    filename=STD_PATH+'last_20_recieved.csv'
    master.to_csv(STD_PATH+'last_20_recieved.csv')
    if master.shape[0]<=0:
        return {'action':'empty'}
    col=master.columns.to_list()
    row=master.index.to_list()
    if get_gen('LOGIN'):
        editable='yes'
        delete_btn='yes'
    else:
        editable='no'
        delete_btn='no'
    data={'editable':editable,'close':'no','delete_btn':delete_btn,'filename':filename
          ,'des_to_display':'last 20 entry in recieve','export_to_csv':'yes','df':master.to_dict(orient='index'),
          'fit_content':'yes','position':'none','editable_column':['date','qty','remark'],'row':row,'column':col}
    return {'action':'success','data':data}
def last10_loco():
    # get 10 recieve from master df and return pl, description, qty
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    try:
        master = pd.read_pickle(STD_PATH+'master')
    except:
        master = pd.DataFrame(
            {'ucode': [], 'timestamp': [], 'date': [], 'date_ordinal': [], 'pl': [], 'description': [],
             'qty': [], 's_ns': [], 'unit': [],  'issued_to': [],
             'loco_number': [], 'rate': [], 'remark': [], 'issue_check': []})
        master.to_pickle(STD_PATH+'master')
    master.sort_values(by='date_ordinal',ascending=False,inplace=True)
    loco_list=master['loco_number'].to_list()
    new_list=[]
    unique=[]
    for i in loco_list:
        if i in new_list:
            unique.append('remove')
        else:
            unique.append('keep')
            new_list.append(i)
    master['remove']=unique
    master=master[master['remove']=='keep']
    # master = master[master['issue_check'] == 'recieve']
    master = master[:10]
    master.set_index('date',inplace=True)
    master = master[['date', 'loco_number']]
    if master.shape[0] <= 0:
        return {'action': 'empty'}
    return {'action': 'success', 'data': master.to_dict()}
def last10_latest():
    # get 10 by date from udf file
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    try:
        udf = pd.read_pickle(STD_PATH+'udf')
    except:
        udf = pd.DataFrame({'date': [], 'pl': [], 'description': [],
                            's_ns': [], 'unit': [], 'rate': [], 'to_be_display': []})
        udf.to_pickle(STD_PATH+'udf')
    udf.sort_values(by='date',ascending=False,inplace=True)
    udf=udf[:10]
    udf['date_str']=str(udf['date'])
    udf.set_index('date_str',inplace=True)
    udf=udf[['pl','description','s_ns','unit','rate']]

    return {'action': 'success', 'data': udf.to_dict()}

def master_filter(i):
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    # data ={date_from:}
    udf = pd.read_pickle(STD_PATH+'udf')
    st='SELECT FROM master '
    pl=i['pl']
    description=i['description']
    date_from=i['date_from']
    date_to=i['date_to']
    # lm_start=i['lm_start']
    # lm_end=i['lm_end']
    s_ns=i['s_ns']
    unit=i['unit']
    loco=i['loco']
    issued_to=i['issued_to']
    issue_check=i['issue_check']
    where={}
    masterdb = db.connect(STD_PATH+'master.db')
    cur = masterdb.cursor()
    if pl=='':
        pass
    else:
        if pl in udf['pl'].to_list():
            pass
        else:
            return {'action':'failed','message':'check pl'}
        if description in udf['description'].to_list():
            pass
        else:
            return {'action': 'failed', 'message': 'check description'}
        where['pl=']=pl
    if date_from=='':
        return {'action':'failed','message':' kindly enter date range'}
    
    date_from=datetime.datetime.strptime(date_from, '%Y-%m-%d').date().toordinal() # small date
    if date_to=='':
        return {'action':'failed','message':' kindly enter date range'}
    date_to=datetime.datetime.strptime(date_to, '%Y-%m-%d').date().toordinal() # large date
    if date_to<=date_from or date_to>datetime.datetime.now().date().toordinal():
        return {'action':'failed','message':'check date'}
    where['date_ordinal>=']=date_from
    where['date_ordinal<=']=date_to
    # if lm_start=='':
    #     pass
    # else:
    #     temp=lm_start.split('.')
    #     try:
    #         isinstance(int(temp[1]),int) and isinstance(int(temp[2]),int)
    #     except:
    #         return {'action':'failed','message':'check lm number'}

    #     lm_start=get_gen('section_name')+'.'+str(int(temp[1]))+'.'+str(int(temp[2]))
    # if lm_end == '':
    #     pass
    # else:
    #     temp = lm_end.split('.')
    #     try:
    #         isinstance(int(temp[1]), int) and isinstance(int(temp[2]), int)
    #     except:
    #         return {'action': 'failed', 'message': 'check lm number'}

    #     lm_end = get_gen('section_name')+'.' + str(int(temp[1])) + '.' + str(int(temp[2]))


    #     st='SELECT MIN(ucode) from master WHERE lm='+db_str(lm_start)
    #     res=cur.execute(st)
    #     res=res.fetchall()
    #     if res[0][0]==None:
    #         return {'action':'failed','message':'check lm'}
    #     else:
    #         lm_start=res[0][0]
    #     st = 'SELECT MAX(ucode) from master WHERE lm=' + db_str(lm_end)
    #     res = cur.execute(st)
    #     res = res.fetchall()
    #     if res[0][0]==None:
    #         return {'action': 'failed', 'message': 'check lm'}
    #     else:
    #         lm_end = res[0][0]
    #     if lm_start<lm_end:#these are ucode now
    #         where['ucode >=']=lm_start
    #         where['ucode <=']=lm_end
    #         where['lm !=']=''
    #         where['i_r_flag=']='recieve'
    if s_ns=='':
        pass
    else:
        where['s_ns=']=s_ns
    if unit=='':
        pass
    else:
        where['unit=']=unit
    if loco=='':
        pass
    else:
        where['loco_number=']=loco
    if issued_to=='':
        pass
    else:
        where['issued_to=']=issued_to
    if issue_check=='':
        pass
    else:
        where['i_r_flag=']=issue_check
    st='SELECT * FROM master WHERE '
    for i,j in where.items():
        st=st+' '+i+''+db_str(j)+' AND'

    st=st[:-3]
    st=st+';'
    res=cur.execute(st)
    res=res.fetchall()
    if len(res)==0:
        return {'action':'failed','message':'no data found'}
    else:
        df = pd.DataFrame({'ucode': [], 'timestamp': [], 'date': [], 'date_ordinal': [], 'pl': [], 'description': [],
                           'qty': [], 's_ns': [], 'unit': [],  'issued_to': [],
                           'loco_number': [], 'rate': [], 'remark': [], 'issue_check': []})
        for i in res:
            df.loc[len(df.index)] = list(i)
        df.set_index('ucode', inplace=True)
        # HERE SET OPENING BALANCE OF STOCK
        df.sort_values(by='date_ordinal', ascending=True, inplace=True)
        df.drop(['timestamp', 'date_ordinal'], axis=1,inplace=True)
        df=convert_to_str(df)
        filename=STD_PATH+'filter.csv'
        df.to_csv(filename)
        col=df.columns.to_list()
        row=df.index.to_list()
        if get_gen('LOGIN'):
            editable='yes'
            delete_btn='yes'
        else:
            editable='no'
            delete_btn='no'
        data={'editable':editable,'close':'yes','delete_btn':delete_btn,'filename':filename
          ,'des_to_display':'RESULT','export_to_csv':'yes','df':df.to_dict(orient='index'),
          'fit_content':'yes','position':'absolute','editable_column':['date','qty','remark'],'row':row,'column':col}
        return {'action':'success','data':data}
def create_template(data):
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    path=STD_PATH+'temp.csv'
    try:
        df=pd.read_csv(path)
    except:
        return {'action':'failure','message':'check file may be corrupt'}
    df_col=list(df.columns)
    if 'pl' in df_col and 'description' in df_col:
        pass
    else:
        return {'action':'failed','message':'pl or description column not found'}
    pl=list(map(lambda x:str(x),df['pl'].to_list()))
    df['pl']=pl
    description=df['description'].to_list()
    udf=pd.read_pickle(STD_PATH+'udf')
    x=[]
    for i in range(len(pl)):
        if pl[i] in udf['pl'].to_list():
            x.append('pl')
        elif description[i] in udf['description'].to_list():
            x.append('description')
        else:
            x.append('not')
    if data['not_found']!='checked' and 'not' in x:
        st='VALUE AT INDEX '
        for i in range(len(x)):
            if x[i]=='not':
                st=st+','+str(i)
        st=st+' NOT FOUND IN STD FILE'
        
        return  {'action':'not_found','message':st}
    df=pd.DataFrame({'pl':['not'],'description':['not'],'unit':['not'],'s_ns':['not'],'rate':['not']})
    df=df[df['pl']!='not']
    for i in range(len(x)):
        if x[i]=='pl':
            temp=udf[udf['pl']==pl[i]]
            pl_1=temp['pl'].to_list()[0]
            des=temp['description'].to_list()[0]
            unit=temp['unit'].to_list()[0]
            rate=temp['s_ns'].to_list()[0]
            s_ns=temp['rate'].to_list()[0]
            df.loc[len(df.index)]=[pl_1,des,unit,s_ns,rate]
        elif x[i]=='description':
            temp=udf[udf['description']==description[i]]
            pl_1=temp['pl'].to_list()[0]
            des=temp['description'].to_list()[0]
            unit=temp['unit'].to_list()[0]
            rate=temp['s_ns'].to_list()[0]
            s_ns=temp['rate'].to_list()[0]
            df.loc[len(df.index)]=[pl_1,des,unit,s_ns,rate]
        else:
            pl_1=pl[i]
            des=description[i]
            unit='not found'
            rate='not found'
            s_ns='not found'
            df.loc[len(df.index)]=[pl_1,des,unit,s_ns,rate]
    path=STD_PATH
    try:
        x=get_gen('template_list')
    except:
        x={}
        store_gen({},'template_list')
    x[data['template_name']]=path+data['template_name']
    store_gen(x,'template_list')
    df.to_pickle(path+data['template_name'])
    return {'action':'success','data':''}
def blank_template(data):
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    no_of_loco=data['loco'].split(',')
    c=[]
    if len(no_of_loco)==1:
        if no_of_loco[0]=='ALL':
            try:
                c=get_gen('loco_list')
            except:
                c=[]
                store_gen(c,'loco_list')
        else:
            try:
                x=int(no_of_loco[0])
                c.append(x)
            except:
                return {'action':'failed','message':'enter correct loco number'}
    else:
        for i in no_of_loco:
            try:
                x=int(i)
                c.append(i)
            except:
                return {'action':'failed','message':'enter correct loco number'}
    if data['template_name']=='udf':
        df=pd.read_pickle(STD_PATH+'udf')
        df=df[['pl','description','unit','s_ns','rate']]
        path=STD_PATH+'temp.csv'
        temp=[]
        for i in df['pl'].to_list():
            temp.append(balance(i))
        df['STOCK']=temp
        temp=[]
        for i in df['pl'].to_list():
            temp.append('')
        for i in c:
            df[i]=temp
        df.to_csv(path)
        return {'action':'success','filename':path,'message':''}
    else:
        x=get_gen('template_list')
        path=x[data['template_name']]
        df=pd.read_pickle(path)
        path=STD_PATH+'temp.csv'
        temp=[]
        for i in df['pl'].to_list():
            temp.append(balance(i))
        df['STOCK']=temp
        temp=[]
        for i in df['pl'].to_list():
            temp.append('')
        
        for i in c:
            df[i]=temp
        
        df.to_csv(path)
        return {'action':'success','filename':path,'message':''}
def delete_template(data):
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    name=data['template_name']
    x=get_gen('template_list')
    path=x[name]
    os.remove(path)
    x.pop(name)
    store_gen(x,'template_list')
    return {'action':'success','data':''}
def filled_template(data):
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    no_of_loco=data['loco'].split(',')
    c=[]
    if len(no_of_loco)==1:
        if no_of_loco[0]=='ALL':
            c=get_loco_list()['loco'].to_list()
        else:
            try:
                x=int(no_of_loco[0])
                c.append(no_of_loco[0])
            except:
                return {'action':'failed','message':'enter correct loco number'}
    else:
        for i in no_of_loco:
            try:
                x=int(i)
                c.append(i)
            except:
                return {'action':'failed','message':'enter correct loco number'}
    if len(c)==0:
        return {'action':'failed','message':'enter correct loco number'}
    unique_list=get_loco_list()
    if unique_list.shape[0]==0:
        return {'action':'failed','message':'no entry'}
    for i in c:
        if i in unique_list['loco'].to_list():
            pass
        else:
            return {'action':'failed','message':str(i)+'loco not found in database'}
    if data['template_name']=='udf':
        template_df=pd.read_pickle(STD_PATH+'udf')
        template_df=template_df[['pl','description','unit','s_ns','rate']]
    else:
        x=get_gen('template_list')
        path=x[data['template_name']]
        template_df=pd.read_pickle(path)
    for i in c:
        temp=[]
        masterdb=db.connect(STD_PATH+'master.db')
        cur=masterdb.cursor()
        st='SELECT date, pl,qty FROM master WHERE loco_number='+db_str(i)+';'
        res=cur.execute(st)
        res=res.fetchall()
        temp_df=pd.DataFrame({'date':[],'pl':[],'qty':[]})
        
        for k in res:
            temp_df.loc[len(temp_df.index)] = list(k)
        cur.close()
        temp_df.set_index('pl',inplace=True)
        for j in template_df.index:
            pl=template_df.loc[j,'pl']
            unit=template_df.loc[j,'unit']
            if unit=='not found':
                temp.append(0)
                continue
            else:
                if pl in temp_df.index:
                    temp.append(temp_df.loc[pl,'qty'])
                else:
                    temp.append(0)
        template_df[i]=temp
    path=STD_PATH+'temp.csv'
    template_df.to_csv(path)
    return {'action':'success','filename':path,'message':''}
def get_loco_list():
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    master_db=db.connect(STD_PATH+'master.db')
    cur=master_db.cursor()
    res=cur.execute("SELECT date,loco_number FROM master WHERE loco_number !='';")
    res=res.fetchall()
    cur.close()
    df=pd.DataFrame({'date':[],'loco':[]})
    for i in res:
        df.loc[len(df.index)] = list(i)
    df.drop_duplicates('loco',keep='first',inplace=True)
    return df
def get_template():
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    try:
        template=get_gen('template_list')
    except:
        template={}
        store_gen({},'template_list')
    name=template.keys()
    return {'action':'success','data':list(name)}
def filled_data_template(data):
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    path=STD_PATH+'temp.csv'
    try:
        df=pd.read_csv(path)
    except:
        return {'action':'failed','message':'check file may be corrupt'}
    try:
        df.drop(['STOCK'], axis=1,inplace=True)
    except:
        pass
    df_col=list(df.columns)
    if 'pl' in df_col and 'description' in df_col:
        pass
    else:
        return {'action':'failed','message':'pl or description column not found'}
    udf=pd.read_pickle(STD_PATH+'udf')
    df['pl']=list(map(lambda x:str(x),df['pl'].to_list()))
    for i in df['pl']:
        if i in udf['pl'].to_list():
            pass
        else:
            return {'action':'failed','message':'check file format'}
    for i in udf['pl']:
        if i in df['pl'].to_list():
            pass
        else:
            return {'action':'failed','message':'check file format'}
    loco=[]
    df.drop_duplicates('pl',keep='first',inplace=True)
    df.set_index('pl',inplace=True)
    for i in df_col:
        if i=='pl' or i=='description' or i=='rate' or i=='unit':
            pass
        else:
            if len(i)==5:
                try:
                    k=int(i)
                    loco.append(i)
                except:
                    return {'action':'failed','data':'unidentified column found '+i}
    try:
        master = pd.read_pickle(STD_PATH+'master')
    except:
        master = pd.DataFrame({'ucode': [], 'timestamp': [], 'date': [],'date_ordinal':[],'pl': [], 'description': [],
                               'qty': [], 's_ns': [], 'unit': [],  'issued_to': [],
                               'loco_number': [], 'rate': [], 'remark': [], 'issue_check': []})
    # data_to_stored = [ucode, timestamp, date_str,date_ordinal, pl, description, qty, s_ns, unit,
    #                   lm, issued_to, loco_number, rate, remark, i_r_flag]
    loco_list=get_loco_list()
    x=[]
    for i in loco:
        if i in loco_list['loco'].to_list() and data['update']!='updated':
            x.append(i)
    if len(x)!=0:    
        return {'action':'data_already_exist','message':'loco no '+str(x)+' data already present'}
    masterdb = db.connect(STD_PATH+'master.db')
    cur = masterdb.cursor()
    ucode=master[-1:]['ucode'].to_list()[0]+1
    date_str=str(datetime.datetime.now().strftime('%d-%m-%Y'))
    if data['update']=='updated':
        for i in loco:
            st='DELETE FROM master WHERE loco_number='+db_str(i)+';'
            cur.execute(st)
            master=master[master['loco_number']!=i]
    for i in loco:
        for j in df.index:
            try:
                if float( df.loc[j,i])<=0:
                    if   float( df.loc[j,i])==0:
                        pass
                    else:
                        return {'action':'failed','message':'error occured while reading value of loco'+i+' pl '+j}
                else:
                    data_to_stored = [ucode, datetime.datetime.now().timestamp(),date_str ,datetime.datetime.now().toordinal(),j, df.loc[j,'description'],float( df.loc[j,i]),df.loc[j,'s_ns'] ,
                                    df.loc[j,'unit'], 'loco', i, float(df.loc[j,'rate']),'', 'issue']
                    master.loc[ucode] = data_to_stored
                    data_to_stored = (ucode, datetime.datetime.now().timestamp(),date_str ,datetime.datetime.now().toordinal(),j, df.loc[j,'description'],float( df.loc[j,i]),df.loc[j,'s_ns'] , df.loc[j,'unit'],
                                      'loco', i, float(df.loc[j,'rate']),'', 'issue')
                    cur.execute("INSERT INTO master VALUES "+str(data_to_stored))
                    ucode=ucode+1
            except:
                masterdb.close()
                return {'action':'failed','message':'error occured while reading value of loco'+i+' pl '+j}
    masterdb.commit()
    masterdb.close()
    master=master[-3000:]
    master.to_pickle(STD_PATH+'master')
    return {'action':'success','message':'entry completed of locos '+str(loco)}
    
def update(data):
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    print('procesiing one request',datetime.datetime.now())
    #  master = pd.DataFrame(
    #             {'ucode': [], 'timestamp': [], 'date': [], 'date_ordinal': [], 'pl': [], 'description': [],
    #              'qty': [], 's_ns': [], 'unit': [], 'lm': [], 'issued_to': [],
    #              'loco_number': [], 'rate': [], 'remark': [], 'issue_check': []})
    col=list(data.keys())
    # editable col=date,timestamp,date_ordinal,qty,remark,rate
    master=pd.read_pickle(STD_PATH+'master')
    masterdb=db.connect(STD_PATH+'master.db')
    cur=masterdb.cursor()
    message=1
    for i in col:
        if i=='date':
            timestamp = datetime.datetime.now().timestamp()
            date_str = data[i]['data'] #'2023-02-22' is format returned from js
            date=datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            date_ordinal=date.toordinal()
            temp=master[master['ucode']==int(data[i]['ucode'])]
            if temp.shape[0]==0:
                continue
            temp=temp.index.to_list()[0]
            master.loc[temp,'date']=date_str
            master.loc[temp,'timesatmp']=timestamp
            master.loc[temp,'date_ordinal']=date_ordinal
            st='UPDATE master SET date='+db_str(date_str)+',date_ordinal='+str(date_ordinal)+',timestamp='+str(timestamp)+' WHERE ucode='+str(data[i]['ucode'])+';'
            cur.execute(st)
            masterdb.commit()
            master.to_pickle(STD_PATH+'master')
        elif i=='qty':
            qty=data[i]['data']
            qty=float(qty).__round__(2)
            temp=master[master['ucode']==int(data[i]['ucode'])]
            if temp.shape[0]==0:
                continue
            temp=temp.index.to_list()[0]
            master.loc[temp,'qty']=qty
            st='UPDATE master SET qty='+str(qty)+' WHERE ucode='+str(data[i]['ucode'])+';'
            cur.execute(st)
            masterdb.commit()
            master.to_pickle(STD_PATH+'master')
        elif i=='remark':
            remark=data[i]['data']
            temp=master[master['ucode']==int(data[i]['ucode'])]
            if temp.shape[0]==0:
                continue
            temp=temp.index.to_list()[0]
            master.loc[temp,'remark']=remark
            st='UPDATE master SET remark='+db_str(remark)+' WHERE ucode='+str(data[i]['ucode'])+';'
            cur.execute(st)
            masterdb.commit()
            master.to_pickle(STD_PATH+'master')
        elif i=='rate':
            rate=data[i]['data']
            rate=float(rate)
            temp=master[master['ucode']==int(data[i]['ucode'])]
            if temp.shape[0]==0:
                continue
            temp=temp.index.to_list()[0]
            master.loc[temp,'rate']=rate
            st='UPDATE master SET rate='+str(rate)+' WHERE ucode='+str(data[i]['ucode'])+';'
            cur.execute(st)
            masterdb.commit()
            master.to_pickle(STD_PATH+'master')
        else:
            message=0
    masterdb.close()
    if message==1:
        return {'action':'success','message':''}
    else:
        return {'action':'failure','message':'some error occured'}
def delete(data):
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    # editable col=date,timestamp,date_ordinal,qty,remark,rate
    master=pd.read_pickle(STD_PATH+'master')
    masterdb=db.connect(STD_PATH+'master.db')
    cur=masterdb.cursor()
    message=1
    master=master[master['ucode']!=int(data['ucode'])]
    master.to_pickle(STD_PATH+'master')
    st='DELETE FROM master WHERE ucode='+data['ucode']
    cur.execute(st)
    masterdb.commit()
    masterdb.close()
    return {'action':'success','message':''}
def entry_show(data):
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    if data=='issue':
        # get 20 issue from master df and return pl, description, qty
        try:
            master = pd.read_pickle(STD_PATH+'master')
        except:
            master = pd.DataFrame(
                {'ucode': [], 'timestamp': [], 'date': [], 'date_ordinal': [], 'pl': [], 'description': [],
                 'qty': [], 's_ns': [], 'unit': [], 'issued_to': [],
                 'loco_number': [], 'rate': [], 'remark': [], 'issue_check': []})
            master.to_pickle(STD_PATH+'master')
        master = master[master['issue_check'] == 'issue']
        master = master[-20:]
        master.set_index('ucode', inplace=True)
        master = master[['date','pl', 'descripton', 'qty', 's_ns', 'unit', 'issued_to','loco_number', 'rate', 'remark']]
        file_name=STD_PATH+'entry_issue.csv'
        master.to_csv(file_name)
        master=convert_to_str(master)
        if master.shape[0] <= 0:
            return {'action': 'empty'}
        return {'action': 'success', 'data': master.to_dict(),'file_id':file_name}
    else:
        # get 20 issue from master df and return pl, description, qty
        try:
            master = pd.read_pickle(STD_PATH+'master')
        except:
            master = pd.DataFrame(
                {'ucode': [], 'timestamp': [], 'date': [], 'date_ordinal': [], 'pl': [], 'description': [],
                 'qty': [], 's_ns': [], 'unit': [],  'issued_to': [],
                 'loco_number': [], 'rate': [], 'remark': [], 'issue_check': []})
            master.to_pickle(STD_PATH+'master')
        master = master[master['issue_check'] == 'recieve']
        master = master[-20:]
        master.set_index('ucode', inplace=True)
        master = master[['date', 'pl', 'descripton', 'qty', 's_ns', 'unit', 'issued_to','loco_number', 'rate', 'remark']]
        file_name = STD_PATH+'entry_issue.csv'
        master.to_csv(file_name)
        master = convert_to_str(master)
        if master.shape[0] <= 0:
            return {'action': 'empty'}
        return {'action': 'success', 'data': master.to_dict(),'file_id':file_name}
def edit_delete_save(option,data):
    if check_start_new():
        return {'action':'failed','message':'setup_incomplete'}
    # option='update,delete, data{ucode:55,column:556}
    if option=='delete':
        ucode=int(data['ucode'])
        masterdb=db.connect(STD_PATH+'master.db')
        master = pd.read_pickle(STD_PATH+'master')
        master=master[master['ucode']!=ucode]
        master.to_pickle(STD_PATH+'master')
        cur=masterdb.cursor()
        st='DELETE master WHERE ucode='+data['ucode']
        cur.execute(st)
        masterdb.commit()
        masterdb.close()
        return {'action':'success'}
    else:
        # when update needed
        # master[['date', 'pl', 'descripton', 'qty', 's_ns', 'unit', 'issued_to', 'loco_number', 'rate', 'remark']]
        # can be changed date,qty,rate,remarks
        date_str = data['date']  # '2023-02-22' is format returned from js
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        date_ordinal = date.toordinal()
        ucode=int(data['ucode'])
        rate=int(data['rate'])
        remark=data['remark']
        if rate<=0:
            return {'action':'failed','message':'invalid rate'}

        master = pd.read_pickle(STD_PATH+'master')
        master = master[master['ucode'] != ucode]
        if master.shape[0]<=0:
            pass
        else:
            temp=master[master['ucode']==ucode].index[0]
            master.loc[temp,'date']=date
            master.loc[temp, 'date_ordinal'] = date_ordinal
            master.loc[temp, 'rate'] = rate
            master.loc[temp, 'remark'] = remark
            # master.loc[temp, 'date'] = date
            master.to_pickle(STD_PATH+'master')
        masterdb = db.connect(STD_PATH+'master.db')
        cur = masterdb.cursor()
        st = 'UPDATE master SET date=' + db_str(date) + ',date_ordinal=' + db_str(date_ordinal) + ' ,rate=' + db_str(
            rate) + ' ,remark=' + db_str(remark) + ', WHERE ucode=' + str(ucode) + ';'
        cur.execute(st)
        masterdb.commit()
        masterdb.close()
        return {'action':'success'}
def convert_to_str(b):
    # it convert dataframe object ro string
    b=b.copy()
    b['index']=b.index
    z = []
    for i in b.columns:
        for j in b[i].to_list():
            z.append(str(j))
        b[i] = z
        z = []
    b.set_index('index',inplace=True)
    # b.drop('index', axis=1, inplace=True)
    return b
def db_str(a):
    if type(a)==str:
        return "'" + a + "'"
    else:
        return  str(a)
def store_gen(data, name):
    location=STD_PATH+'variables'
    try:
        f = open(location, 'rb')
        k = pickle.load(f)
        f.close()
        f = open(location, 'wb')
    except:
        f= open(location, 'wb')
        pickle.dump({}, f)
        f.close()
        f = open(location, 'rb')
        k = pickle.load(f)
        f.close()
        f = open(location, 'wb')
    k[name]=data
    pickle.dump(k, f)
    f.close()
    return 
def get_gen(name):
    location=STD_PATH+'variables'
    f = open(location, 'rb')
    k = pickle.load(f)
    f.close()
    return k[name]
def check_lm():
    if datetime.datetime.now().date().toordinal()>=datetime.datetime.strptime('2023-05-21', '%Y-%m-%d').date().toordinal():
        pass
        # raise Exception('licence Expired')
    store_gen(False,'LOGIN')
    if check_start_new():
        try:
            get_gen('section_name')
        except:
            store_gen('E3 AUX','section_name')
        return {'action':'failed','message':'setup_incomplete'}
    else:
        pass
    # try:
    #     get_gen('section_name')
    # except:
    #     store_gen('E3 AUX','section_name')
    # master=pd.read_pickle(STD_PATH+'master')
    # master=master[master['lm']!='']
    # try:
    #     master=master[-1:]['lm'].to_list()[0]
    # except:
    #     return
    # master=master.split('.')
    # if master[1]==str(datetime.datetime.now().year):
    #     pass
    # else:
    #     lm_set(get_gen('section_name')+'.'+str(datetime.datetime.now().year)+'.1')
    return

# ON START ----------------- TO BE RUN ----


check_lm()

# get_gen('last_lm')
# def map_section_lm(data):
#     store_gen(data['section'],'section_name')
#     return {'action':'success','message':'lm successfully mapped'}
