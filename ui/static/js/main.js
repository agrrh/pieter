var api_url = 'https://pieter.agrrh.com/api/v1';

var api = {
  'get followers' : '/followers/{id}?results={count}',
  'create user'   : '/create',
  'add user'      : '/add/{id}',
  'search'        : '/query/{query}/{/sort}'
};

$('.button')
  .api({
    action: 'get followers'
  })
;

var repos = [];

console.log('Hello');

$( document ).ready(function() {
  hideLoading();
  getReposList();
});

function hideLoading() {
  $("#repos-loading").hide();
}

function displayRepo(repo) {
  $.get(api_url + "repos/" + repo, function(data) {
    console.log(data);
    $('#repo-template').tmpl(data).appendTo('#repos');
    displayRepoScenario(data['name'], data['scenarios']);
  });
}

function displayRepoScenario(repo, scenario) {
  console.log(repo, scenario);
  $("<div class=\"ui grey label\"><i class=\"code icon\"></i> "+scenario+"</div>").appendTo('#repo-' + repo + '-scenarios');
}

function getReposList() {
  $.get(api_url + "repos", function(data) {
    data.forEach(function(item, i, arr) {
      displayRepo(item);
    });
  });
}
