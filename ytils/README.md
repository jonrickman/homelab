PITA to get started, will provide docs later as stuff goes  
_____________  
`docker compose up` will bring whole stack up
_____________

if app is running and working correctly then you should be able to hit `localhost:5001/videos/watch?v={youtube_video_id}` such as `http://localhost:5001/videos/watch?v=DZr1QWkGATg` and it will download a manifest (WIP) and the `.wav` in the `./ytils/app/downloads` folder