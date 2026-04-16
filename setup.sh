mkdir -p ~/.streamlit/

echo "\
[server]\n\
post=$PORT\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml