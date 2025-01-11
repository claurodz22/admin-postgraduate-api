eval "$(ssh-agent -s)";
ssh-add ~/.ssh/claudia_github;
git add .;
# git commit -m "nombre";
git status;
# git push;