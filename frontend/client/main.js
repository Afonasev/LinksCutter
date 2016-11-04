/*
** main.js
*/

const LinkRepository = require('./link').LinkRepository;
const CreateForm = require('./create-form').CreateForm;

const repository = new LinkRepository();
const createForm = new CreateForm(repository);
createForm.runListeners();
