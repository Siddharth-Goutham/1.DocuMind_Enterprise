//async function askAI(){
//    async function uploadFile(){
//
//let file=document.getElementById("fileInput").files[0];
//
//if(!file){
//alert("Please select a file");
//return;
//}
//
//let formData=new FormData();
//formData.append("file",file);
//
//let response=await fetch("http://localhost:8000/upload",{
//method:"POST",
//body:formData
//});
//
//let result=await response.json();
//
//alert(result.message);
//
//}
//
//let input=document.getElementById("question");
//let chat=document.getElementById("chat");
//
//let q=input.value;
//
//if(q==="") return;
//
//chat.innerHTML += "<div class='user'>"+q+"</div>";
//
//input.value="";
//
///* typing animation */
//
//let typing=document.createElement("div");
//typing.className="typing";
//typing.innerHTML="<span></span><span></span><span></span>";
//
//chat.appendChild(typing);
//
///* backend call */
//
//let res=await fetch("http://localhost:8000/ask",{
//method:"POST",
//headers:{"Content-Type":"application/json"},
//body:JSON.stringify({question:q})
//});
//
//let data=await res.json();
//
//typing.remove();
//
//chat.innerHTML += "<div class='ai'>"+data.answer+"</div>";
//
//}