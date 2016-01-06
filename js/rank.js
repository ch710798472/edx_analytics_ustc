/**
 * Created by ch on 16-1-4.
 */
function show_china(){
    select=document.getElementById("china_rank");
    $(select).empty();
    var rankinfo  = $("<div id='rankinfo' style='margin-top:55px;color:blue;font-size: 40px;font-family: sans-serif;'><p align='center'>中国地区Github用户评分排名</p></div>");
    rankinfo.appendTo(select);
    var github_table  = $("<table class='table table-striped'>");
    github_table.appendTo(select);
    var head = $("<thead>");
    head.appendTo(github_table);
    var tr = $("<tr>");
    tr.appendTo(head);

    $("<th>排名</th>").appendTo(tr);
    $("<th>头像</th>").appendTo(tr);
    $("<th>用户名(姓名)</th>").appendTo(tr);
    $("<th>评分</th>").appendTo(tr);
    $("<th>擅长语言</th>").appendTo(tr);
    $("<th>地区</th>").appendTo(tr);
    d3.json("data/userMoreInfo.json", function(data) {
        //data=[{"login":"daimajia","name":"代码家",
        //    "score":"1024","language":"JavaScript","location":"Beijing, China","gravatar":"https://avatars.githubusercontent.com/u/779050?v=3"},
        //    {"login":"daimajia","name":"代码家",
        //        "score":"1024","language":"JavaScript","location":"Beijing, China","gravatar":"https://avatars.githubusercontent.com/u/779050?v=3"},
        //    {"login":"daimajia","name":"代码家",
        //        "score":"1024","language":"JavaScript","location":"Beijing, China","gravatar":"https://avatars.githubusercontent.com/u/779050?v=3"},
        //    {"login":"daimajia","name":"代码家",
        //        "score":"1024","language":"JavaScript","location":"Beijing, China","gravatar":"https://avatars.githubusercontent.com/u/779050?v=3"}];
        for (var i in data) {
                //console.log(data[i]);
                var tr = $("<tr>");
                tr.appendTo(github_table);
                var count = parseInt(i) + 1;
                $("<td class='solid'>NO." + count + "</td>").appendTo(tr);
                $("<td class='solid'>" + "<img height='48' width='48' src=" + data[i]["avatar_url"] + "/>" + "</td>").appendTo(tr);
                $("<td class='solid'>" + "<a href='https://github.com/" + data[i]["login"] + "' target='_blank'>" + data[i]["login"] + "</a>" + "&nbsp(" + data[i]["name"] + ")"+ "</td>").appendTo(tr);
                $("<td class='solid'>" + parseInt(data[i]["score"]) + "</td>").appendTo(tr);
                $("<td class='solid'>" + data[i]["language"] + "</td>").appendTo(tr);
                $("<td class='solid'>" + data[i]["location"] + "</td>").appendTo(tr);
        }
    });
}