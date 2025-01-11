## Pre Push
Para iniciar el ssh-agent 

```
eval "$(ssh-agent -s)";
ssh-add ~/.ssh/claudia_github;
git add .;
git commit -m "descripcion del commit";
git status;
git push;
```

esto se llama markdown