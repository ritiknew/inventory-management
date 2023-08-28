let last20_issue=document.querySelector('#last_20_issue');
let last_20_recieve=document.querySelector('#last_20_recieve');
let last_10_loco=document.querySelector('#last_10_loco');
let latest_items_recieved=document.querySelector('#latest_items_recieved');
let critical_item=document.querySelector('#critical_item');
let inactive_items=document.querySelector('#inactive_items');
let balance=document.querySelector('#balance');
get_data({'function':'s_l_20_issue','data':''}).then(data=>{
    if(data['action']=='success'){
        x=document.createElement('div');
        last20_issue.innerHTML=''
        last20_issue.appendChild(x);
        display_df(x,data['data']);
    }
    else{
        last20_issue.innerHTML=data['message']
        }}
)
get_data({'function':'s_l_20_recieve','data':''}).then(data=>{
    if(data['action']=='success'){
        x=document.createElement('div');
        last_20_recieve.innerHTML=''
        last_20_recieve.appendChild(x);
        display_df(x,data['data']);
    }
    else{
        last20_issue.innerHTML=data['message']
        }}
)
get_data({'function':'last_10_loco','data':''}).then(data=>{
    if(data['action']=='success'){
        x=document.createElement('div');
        last_10_loco.innerHTML=''
        last_10_loco.appendChild(x);
        display_df(x,data['data']);
    }
    else{
        last20_issue.innerHTML=data['message']
        }}
)
get_data({'function':'latest_items_recieved','data':''}).then(data=>{
    if(data['action']=='success'){
        x=document.createElement('div');
        latest_items_recieved.innerHTML=''
        latest_items_recieved.appendChild(x);
        display_df(x,data['data']);
    }
    else{
        last20_issue.innerHTML=data['message']
        }}
)
get_data({'function':'critical_item','data':''}).then(data=>{
    if(data['action']=='success'){
        x=document.createElement('div');
        critical_item.innerHTML=''
        critical_item.appendChild(x);
        display_df(x,data['data']);
    }
    else{
        last20_issue.innerHTML=data['message']
        }}
)
get_data({'function':'inactive_items','data':''}).then(data=>{
    if(data['action']=='success'){
        x=document.createElement('div');
        inactive_items.innerHTML=''
        inactive_items.appendChild(x);
        display_df(x,data['data']);
    }
    else{
        last20_issue.innerHTML=data['message']
        }}
)


get_data({'function':'show_balance','data':''}).then(data=>{
    if(data['action']=='success'){
        x=document.createElement('div');
        balance.innerHTML=''
        balance.appendChild(x);
        display_df(x,data['data']);
    }
    else{
        last20_issue.innerHTML=data['message']
        }}
)



async function get_data(data_to_send){ 
    // console.log('this is before data fetch');
    let k=await fetch(window.location.origin+'/handle',
        {"method":"POST","headers":{"content-Type":"application/json"},
        "body":JSON.stringify({'data':data_to_send})
        }           )
     let m=await k.json()
    //  console.log('this is after data fetch');
     output=m['data']
return output
}
function download_data(filename){
    fetch(window.location.origin+'/down_load',
        {"method":"POST","headers":{"content-Type":"application/json"},
        "body":JSON.stringify({'data':filename})
        }           )
   
    // (B) RETURN AS BLOB
    .then(res => {
      if (res.status != 200) { throw new Error("Bad server response"); }
      return res.blob();
    })
   
    // (C) BLOB DATA
    .then(data => {
      // (C1) "FORCE DOWNLOAD"
      var url = window.URL.createObjectURL(data),
          anchor = document.createElement("a");
        let saveas='download.csv';
      anchor.href = url;
      anchor.download = saveas;
      anchor.click();
   
      // (C2) CLEAN UP
      window.URL.revokeObjectURL(url);
      document.removeChild(anchor);
    })
   
    // (D) HANDLE ERRORS - OPTIONAL
    .catch(err => console.error(err));
}
function display_df(elm,value){
    elm.style.border='5px solid #abe9f5';
    let editable=value.editable;
    let close=value.close;
    let delete_btn=value.delete_btn;
    let filename=value.filename;
    let des_to_display=value.des_to_display;
    let export_to_csv=value.export_to_csv;
    let df=value.df;
    let fit_content=value.fit_content;
    let editable_column=value.editable_column;
    let position=value.position;
    // df={col1:{row1:data,row2:data},col2:{row1:data,row2:data}}
    elm.innerHTML='';
    elm.style.backgroundColor='white';
    let row=value.row;
    if (position=='absolute'){
        elm.style.position='absolute';
        elm.style.zIndex='1000';
        elm.style.backgroundColor='white';
        elm.style.margin='50px 50px 50px 50px';
        elm.style.width='90vw';
        elm.style.height='70vh';
        elm.style.overflowY='scroll';
        elm.style.overflowX='scroll';
        elm.style.backgroundColor='white';
    }
    else{
        elm.style.margin='50px 1px';
    }
    let columns=value.column;
    if (editable=='yes'){
        columns.push('edit');
    }
    if (delete_btn=='yes'){
        columns.push('delete');
    }
    let description_to_display=document.createElement('div');
    description_to_display.innerHTML=des_to_display.toUpperCase();
    description_to_display.style.display='flex';
    description_to_display.style.flexDirection='row';
    description_to_display.style.justifyContent='center';
    description_to_display.style.alignItems='center';

    let btn_div=document.createElement('div');
    btn_div.style.display='flex';
    btn_div.style.flexDirection='row';
    btn_div.style.justifyContent='flex-end';
    btn_div.style.alignItems='center';
    let print_btn=document.createElement('button');
    btn_div.appendChild(print_btn);
    print_btn.innerText='PRINT';
    print_btn.onclick=function (e){
    let a = window.open('', '', 'height=1000, width=1000');
    a.document.write('<html>');
    a.document.write('<body > ');
    
    a.document.write(elm.innerHTML);
    a.document.write('<style>table, th, td {border: 1px solid;}table {width: 100%;border-collapse: collapse;} button{display:none;}</style>')
    a.document.write('</body></html>');
    a.document.close();
    a.print();}
    if(close=='yes'){
        let close_btn=document.createElement('button');
        close_btn.innerText='CLOSE';
        close_btn.style.backgroundColor='#EA4C89';
        close_btn.style.cursor='pointer';

        close_btn.onclick=function (e){elm.innerHTML='';
            elm.style.display='none'}
        btn_div.appendChild(close_btn);
    }
    if(export_to_csv=='yes'){
        let export_btn=document.createElement('button');
        export_btn.innerText='EXPORT TO CSV';
        export_btn.style.backgroundColor='#EA4C89';
        export_btn.style.cursor='pointer';
        export_btn.onclick=function (e){
            download_data(filename);
        }
        btn_div.appendChild(export_btn);
    }
    elm.appendChild(btn_div)
    elm.appendChild(description_to_display);
    let table_body=document.createElement('table');
    elm.appendChild(table_body);
    // row id =row+ucode,row class=row,column id=name,column clas=col,
    // cell id= column+row,row,column,table head class=table_head+div_id
    let table_row_head=document.createElement('tr');
    table_row_head.setAttribute('class','table_head row');
    table_row_head.setAttribute('id','table_head_row'+elm.id);
    // table_row_head.style.backgroundColor='red';
    table_body.appendChild(table_row_head);
    let i=0;
    let j=0;
    let k=0;
    for( i of columns){
        let table_cell_head=document.createElement('th');
        table_cell_head.setAttribute('class','table_head row');
        table_cell_head.setAttribute('id','table_head_row_cell'+i+elm.id);
        table_cell_head.setAttribute('data-column',i);
        table_cell_head.setAttribute('data-row','head');
        table_cell_head.innerText=i.toUpperCase();
        table_row_head.appendChild(table_cell_head);
        // table_cell_head.style.                
    }
    for (i of row){
        let table_row=document.createElement('tr');
        table_row.setAttribute('class','table_row');
        table_row.setAttribute('id','row'+i+elm.id);
        table_row.setAttribute('data-row',i);
        table_body.appendChild(table_row);
        for ( j of columns ){
            if (j=='edit'){
                let table_data=document.createElement('td');
                table_data.setAttribute('class','cell '+'cell'+i+j);
                table_data.setAttribute('id','cell'+elm.id+i+j);
                table_data.setAttribute('data-row',i);
                table_data.setAttribute('data-column',j);
                table_data.style.backgroundColor='#EA4C89';
                table_data.style.cursor='pointer';
                table_data.original=j;
                table_data.innerText='EDIT';
                table_row.appendChild(table_data);
                
                table_data.onclick=function (e){ 
                    row_edit=this.getAttribute('data-row');
                    if (this.innerText=='EDIT'){
                        this.innerText='SAVE';
                        for(k of editable_column){
                            let cell_edit=document.getElementById('cell'+elm.id+row_edit+k);
                            let cell_input=document.createElement('input');
                            cell_input.setAttribute('id','input'+cell_edit.id)
                            if(k=='date'){
                                cell_input.setAttribute('type','date');
                                cell_input.value=cell_edit.original;
                            }
                            else if(k=='qty'){
                                cell_input.setAttribute('type','number');
                                cell_input.value=cell_edit.original;
                            }
                            else{
                                cell_input.setAttribute('type','text');
                                cell_input.value=cell_edit.original;
                            }

                            cell_edit.innerHTML='';
                            cell_edit.appendChild(cell_input);
                        }
                    }
                    else{
                        loader.style.display='block';
                        this.innerText='EDIT';
                        let changes={}
                        let change_flag=0
                        for(k of editable_column){
                            let cell_edit=document.getElementById('cell'+elm.id+row_edit+k);
                            cell_input=document.getElementById('input'+cell_edit.id);
                            if(cell_edit.original!=cell_input.value){
                                changes[k]={'ucode':String(row_edit),'column':String(k),'data':cell_input.value};
                                change_flag=1;

                            }}
                            if (change_flag==1){
                                get_data({'function':'update','data':changes}).then(
                                    data=>{ 
                                    if(data['action']=='success'){
                                        // cell_edit.innerHTML=''
                                        // cell_edit.innerText=cell_input.value;
                                        window.location.reload();
                                    }
                                    else{
                                        alert(data['message']);
                                    }
                                    }
                                )
                                    
                            }
                            else{
                                window.location.reload();

                            }
                        }
                        loader.style.display='none';
                    }
                }

            else if(j=='delete'){
                let table_data=document.createElement('td');
                table_data.setAttribute('class','cell '+'cell'+i+j);
                table_data.setAttribute('id','cell'+elm.id+i+j);
                table_data.setAttribute('data-row',i);
                table_data.setAttribute('data-column',j);
                table_data.original=j;
                table_data.innerText='DELETE';
                table_row.appendChild(table_data);
                table_data.style.backgroundColor='#EA4C89';
                table_data.style.cursor='pointer';
                table_data.onclick=function (e){ 
                    loader.style.display='block';
                    delete_row=this.getAttribute('data-row');
                    if(confirm('Do you want to delete complete row')){
                        get_data({'function':'delete','data':{'ucode':delete_row}}).then(
                            data=>{
                                if(data['action']=='success'){
                                    window.location.reload();
                                }
                                else{
                                    alert(data['message']);
                                    loader.style.display='none';
                                }

                            }
                          
                        ).catch(data=>{
                            loader.style.display='none';}
                        )
                    }
                    else{

                    }
                }}
            else{
                let table_data=document.createElement('td');
                table_data.setAttribute('class','cell '+'cell'+i+j);
                table_data.setAttribute('id','cell'+elm.id+i+j);
                table_data.setAttribute('data-row',i);
                table_data.setAttribute('data-column',j);
                table_data.original=df[i][j];
                table_data.innerText=df[i][j];
                table_row.appendChild(table_data);

            }

        }

    }}