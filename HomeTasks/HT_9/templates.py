base = """
<!doctype html>
<html lang="en">
    <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
        <style>
        {style}
        </style>
        <title>Hacker News | AlexNizovoy's parser</title>
    </head>
    <body>
        <h1>Hacker News</h1>
        <div id="categories" class="container">
            {categories}
        </div>
        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
        <script>
        var acc = document.getElementsByClassName("accordion");
        for (var i = 0; i < acc.length; i++) {
            acc[i].addEventListener("click", function() {
                this.classList.toggle("active");
                var panel = this.nextElementSibling;
                if (panel.style.maxHeight){
                    panel.style.maxHeight = null;
                } else {
                    panel.style.maxHeight = panel.scrollHeight + "px";
                }
                for (var k = 0; k < acc.length; k++) {
                    if ((acc[k] != this) && (acc[k].nextElementSibling.style.maxHeight)) {
                        acc[k].classList.toggle("active")
                        acc[k].nextElementSibling.style.maxHeight = null;
                    }
                }
            });
        }
        </script>
    </body>
</html>
"""

style = """
.accordion {
    background-color: #eee;
    color: #444;
    cursor: pointer;
    padding: 18px;
    width: 100%;
    border: none;
    text-align: left;
    outline: none;
    font-size: 15px;
    transition: 0.4s;
}
.active, .accordion:hover {
    background-color: #ccc;
}
.accordion:after {
    content: '\002B';
    color: #777;
    font-weight: bold;
    float: right;
    margin-left: 5px;
}
.active:after {
    content: "\2212";
}
.panel {
    padding: 0 18px;
    background-color: white;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.2s ease-out;
}
"""

category = """
            <button class="accordion">{name}</button>
            <div class="panel">
                <table>
                    <thead>{table_head}</thead>
                    <tbody>{data}</tbody>
                </table>
            </div>
"""

item = """
<tr>
    <td></td>
</tr>
"""
