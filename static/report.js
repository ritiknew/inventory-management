let option={}
let pl_card_btn=document.getElementById('pl_card');
let master_btn=document.getElementById('master');
let master_filter=document.querySelector('.master_filter');
let pl_card=document.querySelector('.pl_card')
pl_card.style.display='none';
let date_from_master=document.querySelector('#date_from_master');
let date_to_master=document.querySelector('#date_to_master');
let lm_start=document.querySelector('#lm_start');
let lm_end=document.querySelector('#lm_end');
let loco=document.querySelector('#loco');
let pl_master=document.querySelector('.pl_master');
let description_master=document.querySelector('.description_master');
let s_ns=document.querySelector('#stock_check_input');
let unit=document.querySelector('#unit_check_input');
let issued_to=document.querySelector('#loco_issued');
let date_from_pl=document.querySelector('#date_from_pl');
let date_to_pl=document.querySelector('#date_to_pl');
let pl_pl=document.querySelector('.pl_pl');
let description_pl=document.querySelector('.description_pl');
let submit=document.querySelector('#submit')
let issue_check=document.querySelector('#issue_check')
async function match(data){ 
    // console.log('this is before data fetch');
    let k=await fetch(window.location.origin+'/login',
        {"method":"POST","headers":{"content-Type":"application/json"},
        "body":JSON.stringify({'data':data})
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

option.selected='master_filter';
pl_card_btn.onclick=function (e){if(option.selected=='master_filter'){
    pl_card.style.display='flex';
    master_filter.style.display='none';
    pl_card_btn.style.backgroundColor='rgb(146, 18, 153)';
    pl_card_btn.style.color='#f3eeee';
    option.selected='pl_card';
    master_btn.style.backgroundColor='aqua';
    master_btn.style.color='#000';
}}
master_btn.onclick=function (e){if(option.selected=='master_filter'){
    
}
else{
pl_card.style.display='none';
master_filter.style.display='flex';
master_btn.style.backgroundColor='rgb(146, 18, 153)';
master_btn.style.color='#f3eeee';
pl_card_btn.style.backgroundColor='aqua';
pl_card_btn.style.color='#000';
option.selected='master_filter';
}}
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
    let row=value.row;
    elm.style.backgroundColor='white';
    if (position=='absolute'){
        elm.style.position='absolute';
        elm.style.zIndex='1000';
        elm.style.backgroundColor='white';
        elm.style.margin='50px 50px 50px 50px';
        elm.style.width='90vw';
        elm.style.height='70vh';
        elm.style.overflowY='scroll';
        elm.style.overflowX='scroll';
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
    description_to_display.innerHTML=des_to_display.toUpperCase()
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
                                        // window.location.reload();
                                        elm.remove();
                                        submit.click();
                                        loader.style.display='none';
                                    }
                                    else{
                                        alert(data['message']);
                                    }
                                    }
                                )
                                    
                            }
                            else{elm.remove();
                                submit.click();
                                loader.style.display='none';

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
                                        elm.remove();
                                        submit.click();
                                        loader.style.display='none';
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

function autocomplete (ele){
    ele.current_focus=null;
    ele.out=1;
    // let ele.current_focus;
    // set event listner to element input 
    ele.addEventListener('input',function (e){if(ele.value==''){removelist()}
    else{showdata(e)}})
    function showdata(x){
        // let ele.current_focus=0;
        removelist()
        let list_to_show;
        // console.log('this . value',this.value)
        match({'d1':ele.value,'d2':ele.id}).then((data)=>{
            // console.log('current focus',ele.current_focus)
            list_to_show=data[0];
            list_to_hide=data[1];
            // console.log('inside autocomplete',list_to_show)
            let list_=document.createElement('div');
            ele.insertAdjacentElement('afterend',list_);
            list_.setAttribute('id',ele.getAttribute('id')+'list');
            list_.setAttribute('class',ele.getAttribute('class')+'list');
            list_.style.position='absolute';
            list_.style.zIndex='100';
            list_.style.background='white'
            for (let i in list_to_show){
                var list_item=document.createElement('div');
                list_item.innerHTML=list_to_show[i];
                list_item.setAttribute('class',ele.getAttribute('id')+'listitem');
                list_item.setAttribute('id',ele.getAttribute('id')+'listitem'+i);
                list_item.setAttribute('data-pl',list_to_hide[i]);
                list_item.onmouseover=function(e){this.style='background-color:#a4f0e2';
                ele.current_focus=Number(this.id[this.id.length-1]);
                ele.out=0
            }
                list_item.onmouseout=function(e){this.style='background-color:white';
                ele.out=1
                ele.current_focus=null;}
                list_item.onclick=function (e){ele.current_focus=Number(this.id[this.id.length-1]);
                    // console.log('this item clicked',ele.current_focus)
                    selcted_element()};
                list_.append(list_item);
            }
        }
        );
    }

    ele.addEventListener("keydown", function(e) {
        var x = document.getElementById(ele.id + "list");
        if (!x){return;}
        if (e.keyCode == 40) {
            // if down arrow pressed
            let length=x.childElementCount;
            if (ele.current_focus==null){
                ele.current_focus=0;
                list_item=document.getElementById(ele.id + "listitem"+ele.current_focus);
            list_item.style='background-color:#a4f0e2';
            return;

            }

            if (ele.current_focus==length-1 ){
                list_item=document.getElementById(ele.id + "listitem"+ele.current_focus);
                list_item.style='background-color:white';
                ele.current_focus=0;
                list_item=document.getElementById(ele.id + "listitem"+ele.current_focus);
                list_item.style='background-color:#a4f0e2';
                return;
            }
            if (ele.current_focus<length-1){
                list_item=document.getElementById(ele.id + "listitem"+ele.current_focus);
                list_item.style='background-color:white';
                ele.current_focus++;
                list_item=document.getElementById(ele.id + "listitem"+ele.current_focus);
                list_item.style='background-color:#a4f0e2';
                return;
            }
        } else if (e.keyCode == 38) { //up
          /*If the arrow UP key is pressed,
          decrease the ele.current_focus variable:*/
            let length=x.childElementCount;
            // if(!ele.current_focus){ele.current_focus=}
            if (ele.current_focus==null){ele.current_focus=length-1;
                list_item=document.getElementById(ele.id + "listitem"+ele.current_focus);
                list_item.style='background-color:#a4f0e2'; 
                return
            }
            if (ele.current_focus==0){
                list_item=document.getElementById(ele.id + "listitem"+ele.current_focus);
                list_item.style='background-color:white';
                ele.current_focus=length-1;
                list_item=document.getElementById(ele.id + "listitem"+ele.current_focus);
                list_item.style='background-color:#a4f0e2';
                ele.current_focus=length-1;
                return;
            }
            if (ele.current_focus<=length-1){
                list_item=document.getElementById(ele.id + "listitem"+ele.current_focus);
                list_item.style='background-color:white';
                ele.current_focus--;
                list_item=document.getElementById(ele.id + "listitem"+ele.current_focus);
                list_item.style='background-color:#a4f0e2';
                return;
            }
        } else if (e.keyCode == 13) {
          /*If the ENTER key is pressed, prevent the form from being submitted,*/
            selcted_element()
        //   if (ele.current_focus > -1) {
        //     /*and simulate a click on the "active" item:*/
        //     if (x) x[ele.current_focus].click();
        //   }
        }
    })
    function selcted_element(){
        // this function get current focus element and delete all div
        list_item=document.getElementById(ele.id + "listitem"+ele.current_focus);
        ele.value=list_item.innerText;
        loader.style.display='block';
        v_to_be_send=list_item.getAttribute('data-pl');
        get_data({'function':'autocomplete_setup','data':{'data_type':ele.id,'data':v_to_be_send}}).then(data=>{
            if(data['status']=='ok'){
                message=data['data'];
                if(option.selected=='pl_card'){
                    pl_pl.value=message['pl'];
                    description_pl.value=message['description'];
                    loader.style.display='none';
                }
                else{ pl_master.value=message['pl'];
                description_master.value=message['description'];
                s_ns.value=message['s_ns'];
                unit.value=message['unit'];
                loader.style.display='none';}
            }
            if(data['status']=='new'){
                loader.style.display='none';
                option.new='true';
            }
            else{
                loader.style.display='none';
            }
        }).catch(data=>{loader.style.display='none';})
        removelist();
    }
    function removelist(){
        // let x = document.getElementById(ele.id + "list");
        // if (!x){return;}
        let list_=document.getElementById(ele.id + "list");
        while(!!list_){
            
            list_.remove();
            list_=document.getElementById(ele.id + "list");
        }
        return;

    }
    function hide_items(){
        if (ele.out){
            list_=document.getElementById(ele.id + "list");
        if (list_)
        {list_.style.display='none';}}
        // list_=document.getElementById(ele.id + "list");
        // list_.style.display='none';
        return;
    }
    ele.onblur=hide_items
    // ele.onblur=hide_items;
}
submit.onclick=function (e){
    let data_to_send={};
    if(option.selected=='master_filter'){
        data_to_send.pl=pl_master.value;
        data_to_send.description=description_master.value;
        data_to_send.date_from=date_from_master.value;
        data_to_send.date_to=date_to_master.value;
        data_to_send.lm_start=lm_start.value;
        data_to_send.lm_end=lm_end.value;
        data_to_send.s_ns=s_ns.value;
        data_to_send.unit=unit.value;
        data_to_send.loco=loco.value;
        data_to_send.issued_to=issued_to.value;
        data_to_send.issue_check=issue_check.value;
        get_data({'function':'master_filter','data':data_to_send}).then(data=>{
            if(data['action']=='success'){
                let x=document.createElement('div');
                let y=document.getElementById('display_df');
                y.appendChild(x);
                display_df(x,data['data'])
            }
            else{
                alert(data['message'])
            }
        })
        
    }
    else{data_to_send.pl=pl_pl.value;
        data_to_send.description=description_pl.value;
        data_to_send.date_from=date_from_pl.value;
        data_to_send.date_to=date_to_pl.value;
        get_data({'function':'pl_card','data':data_to_send}).then(data=>{
            if(data['action']=='success'){
                let x=document.createElement('div');
                let y=document.getElementById('display_df');
                y.appendChild(x);
                display_df(x,data['data'])
            }
            else{
                alert(data['message'])
            }
        })

    }

}

autocomplete(pl_master);
autocomplete(description_master);
autocomplete(pl_pl);
autocomplete(description_pl);

pl_card_btn.click()