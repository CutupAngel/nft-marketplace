let box = document.querySelector(".box");
let output = document.querySelector(".output");
let fill = document.querySelector(".fill");
let click = document.querySelector("button");
let upload_text = document.querySelector(".upload_text");
let count_area = document.querySelector(".count_area");

click.addEventListener('click',()=>{
    var a = 0;
    var run =setInterval(frames,30);
    function frames(){
        a = a+1;
        if(a == 101){
            clearInterval(run);
            box.style.display = "none";
            output.style.display = "block";
         
        }
        else{
            var counter = document.querySelector(".counter");
            counter.textContent = a + "%";
            fill.style.width = a + "%";
            upload_text.style.display = "none"
            count_area.style.display = "block"
        }
    }
})