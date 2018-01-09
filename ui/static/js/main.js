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

function hideRepos() {
  $("#repos").hide();
}

function displayRepo(repo) {
  $("#repo").show();
  $('#repo').removeClass('three column').addClass('one column');
  $.get(api_url + "repos/" + repo, function(data) {
    console.log(data);
    $("#repo-loading").hide();
    $('#repo-template').tmpl(data).appendTo('#repo');
  });
}

function displayReposRepo(repo) {
  $.get(api_url + "repos/" + repo, function(data) {
    $('#repos-repo-template').tmpl(data).appendTo('#repos');
    displayRepoScenario(data['name'], data['scenarios']);
  });
}

function displayRepoScenario(repo, scenario) {
  scenario.forEach(function(item, i, arr) {
    $("#repo-scenario-template").tmpl({'scenario': item}).appendTo('#repo-' + repo + '-scenarios');
  });
}

function getReposList() {
  $.get(api_url + "repos", function(data) {
    data.forEach(function(item, i, arr) {
      displayReposRepo(item);
    });
  });
}
