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
let container=document.querySelector('.container');
let user_name=document.querySelector('#username');
let password=document.querySelector('#pass');
let submit=document.querySelector('#submit');
let label=document.querySelector('#label');
submit.onclick=function(){
    if (user_name.value=='' || password.value==''){
        return;
    }
    else{
        get_data({'function':'login','data':{'username':user_name.value,'password':password.value}})
        .then(data=>{
            if (data['action']=='success'){
                let x=document.createElement('a')
                x.setAttribute('href','setting');
                x.click();
            }
            else{
                label.innerText='incorrect user name or password'
                
            }
        })
        }
}