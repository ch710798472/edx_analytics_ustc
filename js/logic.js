/**
 * Created by ch on 16-1-3.
 */
//响应不同的请求函数
function devild(i){
    if(document.getElementById("svg1") != null)
        document.body.removeChild(document.getElementById("svg1"));
    if(document.getElementById("svg1.1")!= null)
        document.body.removeChild(document.getElementById("svg1.1"));
    if(document.getElementById("svg2") != null)
        document.body.removeChild(document.getElementById("svg2"));
    if(document.getElementById("svg3") != null)
        document.body.removeChild(document.getElementById("svg3"));
    if(document.getElementById("svg4") != null)
        document.body.removeChild(document.getElementById("svg4"));
    if(document.getElementById("myCarousel") != null)
        document.getElementById("myCarousel").style.display="none";
    if(i ==1) {
        reporect();
    }
    if(i ==2) {
        langpie();
    }
    if(i ==3) {
        langpie();
    }
    if(i ==4) {
        networkx();
    }
}

function getstart(){
    if(document.getElementById("myCarousel").style.display == "none") {
        document.getElementById("myCarousel").style.display = "block";
        if(document.getElementById("svg1") != null)
            document.body.removeChild(document.getElementById("svg1"));
        if(document.getElementById("svg1.1")!= null)
            document.body.removeChild(document.getElementById("svg1.1"));
        if(document.getElementById("svg2") != null)
            document.body.removeChild(document.getElementById("svg2"));
        if(document.getElementById("svg3") != null)
            document.body.removeChild(document.getElementById("svg3"));
        if(document.getElementById("svg4") != null)
            document.body.removeChild(document.getElementById("svg4"));
    }
}

function staticimages(i){
    if(document.getElementById("svg1") != null)
        document.body.removeChild(document.getElementById("svg1"));
    if(document.getElementById("svg1.1")!= null)
        document.body.removeChild(document.getElementById("svg1.1"));
    if(document.getElementById("svg2") != null)
        document.body.removeChild(document.getElementById("svg2"));
    if(document.getElementById("svg3") != null)
        document.body.removeChild(document.getElementById("svg3"));
    if(document.getElementById("svg4") != null)
        document.body.removeChild(document.getElementById("svg4"));
    if(document.getElementById("myCarousel") != null)
        document.getElementById("myCarousel").style.display="none";
    if(i == 1){
        document.getElementById("insert").innerHTML='<img src="../images/nation_count.png" height="800" width="1000" />';
    }
}