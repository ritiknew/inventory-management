let create_template_file=document.querySelector('#create_template_file');
let upload_template_create_button=document.querySelector('#upload_template_create_button');
let template_select_get=document.querySelector('#template_select_get');
let template_select_delete=document.querySelector('#template_select_delete');
let template_select_upload=document.querySelector('#template_select_upload');
let get_blank_format_btn=document.querySelector('#blank_template');
let filled_template_btn=document.querySelector('#filled_template');
let loco_get=document.querySelector('#loco_get');
let template_name=document.querySelector('#template_name');
let loader=document.getElementById('loader');
let upload_template_button=document.querySelector('#upload_template_button');
let upload_template=document.querySelector('#upload_template')
let delete_template=document.querySelector('#delete_template')


// let template_select_get=document.querySelector('#template_select_get');
upload_template_create_button.onclick=function (e){
if(template_name.value=='' || template_name.value=='master'){
  alert('ENTER TEMPLATE NAME');
  return;}
else if(create_template_file.value==''){
  alert('select file');
  return;

}
else{
  let filename=create_template_file.value;
  filename=filename.split('.')
  filename=filename[filename.length-1];
  if (filename!='csv'){
    alert('Only csv file support')
  }
  else{
    loader.style.display='block';
    upload(create_template_file.files).then(data=>{
      if(data['action']=='success'){
        get_data({'function':'create_template','data':{'template_name':template_name.value,'not_found':'not_checked'}})
        .then(
          data_1=>{if (data_1['action']=='success'){
            template_name.value=='';
            create_template_file.value='';
            window.location.reload()
            loader.style.display='none';
          }
          else{
            if(data_1['action']=='not_found'){
              if(confirm('many valued not found in standard file.'+data_1['message']))
              {get_data({'function':'create_template','data':{'template_name':template_name.value,'not_found':'checked'}})
              .then(
                data_2=>{if (data_2['action']=='success'){
                  template_name.value=='';
                  create_template_file.value='';
                  window.location.reload()
                  loader.style.display='none';
                }
                else{
                  alert(data_1['message']);
            loader.style.display='none';
                }})

              }
            }
            else{
            alert(data_1['message']);
            loader.style.display='none';
          }}

          }
        )
      }
      else{
        loader.style.display='none';
      }
      })
  }
}
      
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
upload_template_button.onclick=function (e){
  if(template_select_upload.value==''){
    alert('SELECT TEMPLATE NAME');
    return;}
  else if(upload_template.value==''){
    alert('select file');
    return;
  }
  else{
    let filename=upload_template.value;
    filename=filename.split('.')
    filename=filename[filename.length-1];
    if (filename!='csv'){
      alert('Only csv file support')
    }
    else{
      loader.style.display='block';
      upload(upload_template.files).then(data=>{
        if(data['action']=='success'){
          get_data({'function':'filled_data_template','data':{'template_name':template_select_upload.value,'update':'not checked'}})
          .then(
            data_1=>{if (data_1['action']=='success'){
              alert(data_1['message'])
              upload_template.value='';
  
              loader.style.display='none';
            }
            else if(data_1['action']=='data_already_exist'){
              if (confirm(data_1['message']+'do you wnat to update if ok then all data will be updated')){
              get_data({'function':'filled_data_template','data':{'template_name':template_select_upload.value,'update':'updated'}})
              .then(
                data_2=>{if (data_2['action']=='success'){
                  alert(data_2['message'])
                  upload_template.value='';
      
                  loader.style.display='none';
                }
            
            else {alert(data_2['message']);
            loader.style.display='none';}
            })}
            else{
              return;
            }}
            else{
              alert(data_1['message']);
              loader.style.display='none';
            }
  
            }
          )
        }
        else{alert(data['message']);
          loader.style.display='none';
        }
        })
    }
  }
        
}
delete_template.onclick=function (e){
  if(template_select_delete.value=='' || template_select_delete.value=='udf' ){
    alert('SELECT TEMPLATE NAME');
    return;}
  else{
    if(confirm('Do you want to delete selected template')){
      get_data({'function':'delete_template','data':{'template_name':template_select_delete.value}})
      .then(data=>{
        if(data['action']=='success'){
          window.location.reload();
        }
        else{alert(data['message'])}
      })
    }
    else{}
  }}

get_blank_format_btn.onclick=function (e){
  if(loco_get.value==''){
    alert('ENTER LOCO NUMBER');
    return;}
  else if(template_select_get.value==''){
    alert('select template');
    return;
  }
  else{ loader.style.display='block';
    get_data({'function':'blank_format','data':{'template_name':template_select_get.value,'loco':loco_get.value}})
          .then(
            data=>{if (data['action']=='success'){
              download_data(data['filename'])
              loco_get.value='';
              template_select_get.value='';
              loader.style.display='none';
            }
            else{
              alert(data['message']);
              loader.style.display='none';
            }
        })
    }
  }
  filled_template_btn.onclick=function (e){
    if(loco_get.value==''){
      alert('ENTER LOCO NUMBER');
      return;}
    else if(template_select_get.value==''){
      alert('select template');
      return;
    }
    else{ loader.style.display='block';
      get_data({'function':'filled_template','data':{'template_name':template_select_get.value,'loco':loco_get.value}})
            .then(
              data=>{if (data['action']=='success'){
                download_data(data['filename'])
                loco_get.value='';
                template_select_get.value='';
                loader.style.display='none';
              }
              else{
                alert(data['message']);
                loader.style.display='none';
              }
          })
      }
    }
  
async function upload(files){
  // const files = upload_template_create.files;
  let formData = new FormData()
  formData.append('myFile', files[0])
  let k= await fetch(window.location.origin+'/upload', {
    method: 'POST',
    body: formData
  })
  let m=await k.json()
  //  console.log('this is after data fetch');
return m

}
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

get_data({'function':'get_template_list','data':''}).then(data=>{
    if(data['action']=='success'){
        let no_template=data['data'];
        for( let i of no_template ){
            let x=document.createElement('option');
            x.value=i;
            x.innerText=i;
            template_select_delete.appendChild(x);
            x=document.createElement('option');
            x.value=i;
            x.innerText=i;
            template_select_get.appendChild(x);
            x=document.createElement('option');
        }
    }
})
