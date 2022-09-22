# Epidemic modelling with lambda functions
Half-baked solution for a back-end epidemic simulator using aws lambda.
AWS lambda functions, using the serverless framework, was completely the wrong approach.
Namely, becuase computer runtime exceeds 30s and AWS API gateway is limited to 30 seconds max.
Moreover, to animate the frames matplot lib requires installation to some video processing libraray installed (such as ffmpeg).
After animating, the video needs to be uploaded, which again takes precious time.
Therefore, AWS lambda is unuseable, at least without having some hideous work-around.
