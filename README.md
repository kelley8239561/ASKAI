# ASKAI Introduction
Assistant Show Keen AI

# <<<automatic task>>>
 ## 1. task recognization
 - input: language instructions
 - output: task list
 ## 2. task plan(cross page/app)
 - input: task and pagelist
 - output: page/app list and objectives
 ## 3. page/app analysis
 - input: page/app screenshots 
 - output: structured page/app and description
 ## 4. task plan(inside page/app)
 - input: structured page/app and description and objective
 - output: action list
 ## 5. action execution
 - input: action list
 - output: page/app screenshots
 ## 6. examination
 - input: page/app screenshots and objective
 - output: True or False

# <<<MM communication>>>
 ## to do(for developer)
 - other models
    - asr
    - tts
    - chat
 - config optimize
 - 

# <<<recording>>>
 ## 1. screen
 ## 2. voice
 ## 3. action

# <<<models>>>
 ## to do(for developer)
 - intention reconization model at Terminal
 - multimodel at Cloud

 ## 1. Chat Model(C)
  ### io
  - text to text
  ### goals
  - communicate without purpose
  - communicate with purpose
    - notification
    - getting information
  ### glm-4

 ## 2. Grounding Model(T)
  ### io
  - (image,text) to text
  ### goals
  - Getting items position in screenshots
  ### GroundingDINO


 ## 3. Extract Model(C&T)
  ### io
  - (image, text) to text
  ### goals
  - task extraction
  - long-term memory generation
  - record extraction

 ## 4. Plan Model(C&T)
  ### io
  - (image,text) to text
  ### goals
  - app decision
  - page decision
  - next operation decision

 ## 5. Route Model(T)
  ### io
  - text to text
  ### goals
  - route the prompter
  - set the task priority