/**
 * Created by ch on 16-1-4.
 */
function show_china(){
    select=document.getElementById("china_rank");
    $(select).empty();
    var github_table  = $("<table class='table table-striped'>");
    github_table.appendTo(select);
    var head = $("<thead>");
    head.appendTo(github_table);
    var tr = $("<tr>");
    tr.appendTo(head);

    $("<th>Rank</th>").appendTo(tr);
    $("<th>Avatar</th>").appendTo(tr);
    $("<th>Name</th>").appendTo(tr);
    $("<th>Score</th>").appendTo(tr);
    $("<th>Language</th>").appendTo(tr);
    $("<th>Location</th>").appendTo(tr);
    data=[{"login":"daimajia","name":"代码家",
        "score":"1024","language":"JavaScript","location":"Beijing, China","gravatar":"https://avatars.githubusercontent.com/u/779050?v=3"},
        {"login":"daimajia","name":"代码家",
            "score":"1024","language":"JavaScript","location":"Beijing, China","gravatar":"https://avatars.githubusercontent.com/u/779050?v=3"},
        {"login":"daimajia","name":"代码家",
            "score":"1024","language":"JavaScript","location":"Beijing, China","gravatar":"https://avatars.githubusercontent.com/u/779050?v=3"},
        {"login":"daimajia","name":"代码家",
            "score":"1024","language":"JavaScript","location":"Beijing, China","gravatar":"https://avatars.githubusercontent.com/u/779050?v=3"}];
    for (var i in data){
        var tr = $("<tr>");
        tr.appendTo(github_table);
        var count = parseInt(i) + 1;
        $("<td class='solid'>#" + count + "</td>").appendTo(tr);
        $("<td class='solid'>" + "<img height='48' width='48' src=" + data[i]["gravatar"] + "/>" + "</td>").appendTo(tr);
        $("<td class='solid'>" + "<a href='https://github.com/" + data[i]["login"] + "' target='_blank'>" + data[i]["login"] + "</a>" + "&nbsp(" + data[i]["name"] + ")" + "</td>").appendTo(tr);
        $("<td class='solid'>" + parseInt(data[i]["score"]) + "</td>").appendTo(tr);
        $("<td class='solid'>" + data[i]["language"] + "</td>").appendTo(tr);
        $("<td class='solid'>" + data[i]["location"] + "</td>").appendTo(tr);
    }
}