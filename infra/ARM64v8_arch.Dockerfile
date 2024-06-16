FROM arm64v8/nginx:1.24

COPY nginx.conf /etc/nginx/templates/default.conf.template
