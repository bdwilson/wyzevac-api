# Wyze Vacuum Simple REST API
This REST API uses the [wyze-api](https://pypi.org/project/wyze-sdk/) python 3.9 library.

I am not a Python programmer; this is really bad code. Please fix it. There is
no authentication because the expectation is that you're running this on your
internal, trusted home network. You've been warned.

# Installation (Docker)
1. Grab the [Dockerfile](https://raw.githubusercontent.com/bdwilson/wyzevac-api/master/Dockerfile) via wget and put it in a directory on your Docker server. Then run the commands
below from that directory
2. <code> # docker build -t wyzevac-api --build-arg WYZEVAC_USER='your@email.address' --build-arg WYZEVAC_PASS='your_password' .</code> __Don't forget the dot at the end!__ CTRL-C out of it when it's complete
Optional arguments are WYZEVAC_PORT. You will need to use your email and
password that you use with the Wyze app already. These will default to us, na,
and 59354. 
3. Run your newly created image: <code> # docker run -d --restart unless-stopped -p 59354:59354 --name wyzevac-api -t wyzevac-api</code> (if you changed the port when you built your image, you should also change it here)
4. That's it. If you need to troubleshoot your docker image, you can get into
it via:
<code> # docker exec -it wyzevac-api /bin/bash</code> or 
<code># docker run -it wyzevac-api /bin/bash</code> and then poke around and

# Usage
You'll need to get the IP address of your docker host, then navigate to:
http://your.ip.address:59354/api/list - this should show you your device ID's
on your account, then make subsequent calls with the device id.
<pre>
Usage: /api/[deviceid]/[clean|charge|pause|rooms|suction]

- /api/list will list you devices on your account.

- /api/JA_RO2_XXXXXXXXX/rooms lists rooms with ID numbers

- "clean" takes optional additional arguments of room #'s comma separated
   /api/JA_RO2_XXXXXXXXX/clean/12,13,14

- "suction" takes optional arguments quiet, standard, strong
   /api/JA_RO2_XXXXXXXXX/suction/quiet

- "battery" returns a string representing percentage battery
   remaining

- "mode" returns VacuumMode.SWEEPING if sweeping, VacuumMode.IDLE if idle/charging,
   VacuumMode.ON_WAY_CHARGE if returning to charge, VacuumMode.PAUSE іf stuck
   and needs help
</pre>

# Hubitat
Use the [http get switch](https://github.com/hubitat/HubitatPublic/blob/master/examples/drivers/httpGetSwitch.groovy)
to have an on/off switch using the above commands. __You use the urls above but without the "curl -s"__. You may also use Rule Machine to make HTTP calls. You can also link these to
Amazon Alexa so you can have the N79S features on the N79.

Bugs/Contact Info
-----------------
Bug me on Twitter at [@brianwilson](http://twitter.com/brianwilson) or email me [here](http://cronological.com/comment.php?ref=bubba).
