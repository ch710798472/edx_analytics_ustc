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
    d3.json("data/user.json", function(data) {
        //data=[{"login":"daimajia","name":"代码家",
        //    "score":"1024","language":"JavaScript","location":"Beijing, China","gravatar":"https://avatars.githubusercontent.com/u/779050?v=3"},
        //    {"login":"daimajia","name":"代码家",
        //        "score":"1024","language":"JavaScript","location":"Beijing, China","gravatar":"https://avatars.githubusercontent.com/u/779050?v=3"},
        //    {"login":"daimajia","name":"代码家",
        //        "score":"1024","language":"JavaScript","location":"Beijing, China","gravatar":"https://avatars.githubusercontent.com/u/779050?v=3"},
        //    {"login":"daimajia","name":"代码家",
        //        "score":"1024","language":"JavaScript","location":"Beijing, China","gravatar":"https://avatars.githubusercontent.com/u/779050?v=3"}];
        for (var i in data) {
            for(var j in data[i]){
                console.log(data[i][j]);
                var tr = $("<tr>");
                tr.appendTo(github_table);
                var count = parseInt(j) + 1;
                $("<td class='solid'>NO." + count + "</td>").appendTo(tr);
                $("<td class='solid'>" + "<img height='48' width='48' src=" + data[i][j]["avatar_url"] + "/>" + "</td>").appendTo(tr);
                $("<td class='solid'>" + "<a href='https://github.com/" + data[i][j]["login"] + "' target='_blank'>" + data[i][j]["login"] + "</a>" + "</td>").appendTo(tr);
                //+ "&nbsp(" + data[i]["name"] + ")"
                $("<td class='solid'>" + parseInt(data[i][j]["score"]) + "</td>").appendTo(tr);
                $("<td class='solid'>" + data[i][j]["language"] + "</td>").appendTo(tr);
                $("<td class='solid'>" + data[i][j]["location"] + "</td>").appendTo(tr);
            }
        }
    });
}