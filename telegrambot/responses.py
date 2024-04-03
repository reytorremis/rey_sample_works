#  ------------------ Libraries ------------------------------
from datetime import datetime as dt
import datetime
import db_connection_details as dbd

#  ------------------ Variables ------------------------------
f = "%d/%m/%Y %H:%M:%S"                     # date format
time_out = datetime.timedelta(minutes=5)    # time duration, set to 1 minute

ran_quotes = [

    "Mas Radikal ang magmahal. -Leni Robredo",

    "Ang daming kaguluhan sa paligid. I'm focused on the targets, I keep my eye on the ball. I will not allow myself to be distracted by all of this. -Leni Robredo",

    "You do not lose sight of what you believe in, you do not lose sight of the goal. You drown out the voices, because there are bigger battles to fight. -Leni Robredo",

    "Robredo on vote buying: Take the money, but vote according to conscience. -Leni Robredo",

    "Sa panahon ng matinding hidwaan, ang pagkakaisa ng ating bansa ang tanging pag-asa.-Leni Robredo",

    "I will apologize for any wrongdoing I may have done that may have caused anyone pain or harm... However, I can only speak for myself. I cannot apologize for anyone. -Bongbong Marcos",

    "Wag na ninyong pansinin yang mga vote-buying na 'yan. Kunin yung pera, kung sakali. Pero, 'wag kayong boboto sa sinasabi niya. Iboto ninyo yung gusto ninyo -Bongbong Marcos (2016)",
    "People no longer ask about martial law. They are interested in the current problems of the country such as jobs and traffic.-Bongbong Marcos",
    "Always forgive your enemies; nothing annoys them so much.-Bongbong Marcos quotes Oscar Wilde",
    "Will I say sorry for the thousands and thousands of kilometers that were built? Will I say sorry for the agricultural policy that brought us to self-sufficiency in rice? Will I say sorry for the power generation? Will I say sorry for the highest literacy rate in Asia? What am I to say sorry about? -Bongbong Marcos",

    "The ultimate test of a person's character: give him power and offer him money. If he passes the tes, he is the 'Leader we need'.-Ping Lacson",
    "Aayusing ang gobyerno, aayusin ang buhay ng Pilipino.-Ping Lacson",
    "We cannot anymore afford a ‘more of the same’ brand of leadership during this crucial time in our nation’s history. We should know by now that it doesn’t work. -Ping Lacson",
    "Sin Tax: If only we can tax all the sins of congressmen and senators, we can collect more than enough to cover the entire national budget. -Ping Lacson",
    "What is right must be kept right; what is wrong must be set right. -Ping Lacson",

    "Life is meant to be a challenge because challenges are what make you grow. -Manny Pacquiao",
    "Fearless is getting back up and fighting for what you want over and over again, even though every time you’ve tried before you’ve lost. -Manny Pacquiao",
    "I've already established my (political)machinery. It's like a car. It's fixed already. You just have to get in and drive it. -Manny Pacquiao",
    "Hindi natin masusugpo ang kahirapan kung hindi natin masusugpo ang kurapsyon. -Manny Pacquiao",
    "Miracles do happen. Dreams do come true. -Manny Pacquiao",

    "A leader must not only think outside the box, he must also choose people outside his circle. -Isko Moreno",
    "I will be a healing President. While ours will be a government of national reconstruction, it will also be a government of national reconciliation. Hindi ko isisisi sa nakaraan ang problemang ating kakaharapin. -Isko Moreno",
    "I believe people should speak truth to power rather than threatening the people for speaking the truth. -Isko Moreno",
    "When assaulted with lies, the truth, not the trolls, will set you free. -Isko Moreno",
    "I will be energizing millennials to join the government so that they can put their talent in the service of government. -Isko Moreno"]

"""References

https://mb.com.ph/2021/09/30/we-need-leaders-not-pretenders-says-presidential-hopeful-lacson-as-filing-of-cocs-begins-oct-1/
https://newsinfo.inquirer.net/1125010/lacsons-wishful-thinking-tax-all-sins-of-congressmen-senators
https://newsinfo.inquirer.net/1526848/lacson-warns-vote-buying-can-lead-to-miserable-lives-bad-governance
https://www.awakenthegreatnesswithin.com/35-inspirational-manny-pacquiao-quotes-on-success/
https://www.brainyquote.com/quotes/manny_pacquiao_426287
https://www.instagram.com/p/CXQ4FlEguCH/
https://www.instagram.com/p/CWlaUqDghXe/
https://news.abs-cbn.com/news/09/22/21/list-iskos-quotes-of-note-at-2022-campaign-launch
https://www.facebook.com/photo.php?fbid=474913373991122&set=pb.100044173909089.-2207520000..&type=3
https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.spot.ph%2Fnewsfeatures%2Fthe-latest-news-features%2F66861%2Fquotes-of-the-week-july-1-a125-20160701%3Ffbclid%3DIwAR3_C0EhYUVgJogbFt8ahZzUyUsN4Y-nkQWIyZmm00nVkotfmahgc6vWx-c&h=AT0iyo3lgqfu8yUkprOl52Z-BFYffCoQ-PJu9XqKrih-9ScY45eVJj_5kS3MLXNQj3LRYiGShinV73vrR4_jiLUt2kQAjn0cNKan2Tuh59BV6PA7ejg6NeGLSj1g5ZRJ-kPfKQ
https://l.facebook.com/l.php?u=https%3A%2F%2Fcoconuts.co%2Fmanila%2Fnews%2Flist-bongbong-marcos-top-5-controversial-martial-law-soundbites%2F%3Ffbclid%3DIwAR0nau__A8n0fZJoF1lt6yPc80Kp2NoUziUSbkVUU86chegzGDJ-64370FE&h=AT0iyo3lgqfu8yUkprOl52Z-BFYffCoQ-PJu9XqKrih-9ScY45eVJj_5kS3MLXNQj3LRYiGShinV73vrR4_jiLUt2kQAjn0cNKan2Tuh59BV6PA7ejg6NeGLSj1g5ZRJ-kPfKQ
https://l.facebook.com/l.php?u=https%3A%2F%2Fpolitics.com.ph%2Fbongbong-marcos-forgiveness-the-sweetest-revenge%2F%3Ffbclid%3DIwAR2xRjPVIkiJK2w5FmpWO_9Zap9W470Z7BugqJvgmeAh_557X0RPC4GQPZA&h=AT0iyo3lgqfu8yUkprOl52Z-BFYffCoQ-PJu9XqKrih-9ScY45eVJj_5kS3MLXNQj3LRYiGShinV73vrR4_jiLUt2kQAjn0cNKan2Tuh59BV6PA7ejg6NeGLSj1g5ZRJ-kPfKQ
https://l.facebook.com/l.php?u=https%3A%2F%2Fcoconuts.co%2Fmanila%2Fnews%2Flist-bongbong-marcos-top-5-controversial-martial-law-soundbites%2F%3Ffbclid%3DIwAR1qAzmfVG0HgXkIYgKNine-yZXG9lGcWA7NopuZy8tvZn7FMW6LWD8tn0Y&h=AT0iyo3lgqfu8yUkprOl52Z-BFYffCoQ-PJu9XqKrih-9ScY45eVJj_5kS3MLXNQj3LRYiGShinV73vrR4_jiLUt2kQAjn0cNKan2Tuh59BV6PA7ejg6NeGLSj1g5ZRJ-kPfKQ


"""

#  ------------------ Functions ------------------------------
# Check if current time - last activity time exceeds time out
# last activity is the last message / command (excluding log in and log out)
# For example, you said hellow (unrecognized message) it will still treat that as an activity

def check_for_time_out(phone_number):
    global time_out
    global current_time
    _last_act = dbd.get_last_activity(phone_number)
    last_act = dt.strptime(_last_act.strftime(f),f)
    _current_time = datetime.datetime.now()
    current_time = dt.strptime(_current_time.strftime(f), f)
    if current_time - last_act < time_out:
        print(current_time)
        print(last_act)
        print(str(current_time - last_act))
        return True
    else:
        return False

# List of sample responses such as hi. hello and sup -- only for testing purposes
def sample_responses(input_text):
    user_message = str(input_text).lower()
    if user_message in ("hello","hi","sup"):
        return "Hey! How it's going?"

    if user_message in ("who are you?", "who are you"):
        return "I am Alpha Bot"

    if user_message in ("time", "time?"):
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
        return str(date_time)

    return "I don't understand you!"