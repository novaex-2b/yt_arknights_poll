import pytchat
import curses
from curses import wrapper
from fuzzywuzzy import process
from argparse import ArgumentParser

OPERATORS = ['12F','Aak','Absinthe','Aciddrop','Adnachiel','Akafuyu','Ambriel','Amiya','Andreana','Angelina','Ansel','Aosta','April','Archetto',
             'Arene','Asbestos','Ash','Ashlock','Astesia','Astgenne','Aurora','Ayerscarpe','Bagpipe','Beagle','Beanstalk','Beehunter','Beeswax',
             'Bena','Bibeak','Bison','Blacknight','Blaze','Blemishine','Blitz','Blue Poison','Breeze','Broca','Bubble','Cantabile','Cardigan',
             'Carnelian','Castle-3','Catapult','Ceobe','Ceylon','Chen','Chiave','Click','Cliffheart','Conviction','Corroserum','Courier',
             'Croissant','Cuora','Cutter','Czerny','Deepcolor','Dobermann','Dur-nar','Durin','Dusk','Earthspirit','Ebenholz','Elysium',
             'Enforcer','Erato','Estelle','Ethan','Eunectes','Executor','Exusiai','Eyjafjalla','Fang','Fartooth','FEater','Fiammetta',
             'Firewatch','Flamebringer','Flametail','Flint','Folinic','Franka','Frost','Frostleaf','Gavial','Gitano','Gladiia','Glaucus','Gnosis',
             'Goldenglow','Grani','Gravel','GreyThroat','Greyy','Gummy','Haze','Heavyrain','Heidi','Hellagur','Hibiscus','Honeyberry','Horn',
             'Hoshiguma','Hung','Ifrit','Indigo','Indra','Irene','Iris','Istina','Jackie','Jaye','Jessica','Justice Knight','Kafka','Kaltsit',
             'Kazemaru','Kirara','Kjera','Kroos','La Pluma','Lancet-2','Lappland','Lava','Lee','Leizi','Leonhardt','Ling','Liskarm','Magallan',
             'Manticore','Matoimaru','Matterhorn','May','Mayer','Melantha','Meteor','Meteorite','Midnight','Minimalist','Mint','Mizuki',
             'Mostima','Mountain','Mousse','Mr. Nothing','Mudrock','Mulberry','Myrrh','Myrtle','Młynar','Nearl','Nian','Nightingale','Nightmare',
             'Nine-Colored Deer','Noir Corne','Orchid','Pallas','Passenger','Perfumer','Phantom','Pinecone','Pith','Platinum','Plume','Podenco',
             'Popukar','Pozëmka','Pramanix','Projekt Red','Provence','Proviso','Ptilopsis','Pudding','Purestream','Quercus','Rangers','Reed',
             'Caster','Logistics','Melee','Sniper','Roberta','Robin','Rockrock','Rope','Rosa','Rosmontis','Saga','Saileach','Saria','Savage','Scavenger',
             'Scene','Schwarz','Sesa','Shalem','Shamare','Sharp','Lunacub','Qanipalaat','Quartz','Penance','Vigil','Highmore']
CONFIDENCE = 68

def poll_table(poll_results):
  result = ""
  table_padding = len(sorted(poll_results.keys(),key=len)[-1]) + 2
  for op in poll_results:
    padding = " " * (table_padding - len(op))
    total_votes = sum(poll_results.values())
    operator_str = ""
    if total_votes < 1:
      operator_str = op + padding + ": [{:2d}|{:5.1f}%]".format(poll_results[op],0)
    else:
      percent_vote = poll_results[op] / sum(poll_results.values()) * 100
      operator_str = op + padding + ": [{:2d}|{:5.1f}%]".format(poll_results[op],percent_vote)
    result = result + operator_str + "\n"
  result = result + "\nPress any key to end poll..."
  return result

def run_poll(vid_id,poll_options):
  stdscr.nodelay(True)
  stdscr.addstr(0,0,poll_table(poll_options))
  stdscr.refresh()

  voters = []
  chat = pytchat.create(video_id=vid_id)
  while chat.is_alive():
    key = stdscr.getch()
    if key != -1:
      break
    for c in chat.get().sync_items():
      if ("!vote" in c.message and c.author.name not in voters):
        voters.append(c.author.name)
        user_vote = c.message.split("!vote")[1].lstrip()
        fuzzy_vote = process.extractOne(user_vote, poll_options.keys())
        if fuzzy_vote[1] < CONFIDENCE:
          continue
        else:
          poll_options.update({fuzzy_vote[0]: (poll_options[fuzzy_vote[0]] + 1)})
          stdscr.addstr(0,0,poll_table(poll_options))
          stdscr.refresh()

def poll_manager(args):
  poll_options = {}
  if args.choices:
    for choice in args.choices:
      poll_options.update({choice: 0})
  else:
    for op in OPERATORS:
      poll_options.update({op: 0})
  wrapper(run_poll(args.video,poll_options))

if __name__ == "__main__":
  parser = ArgumentParser(description="a hopefully low latency arknights poll for youtube chat")
  parser.add_argument('video',metavar='ID',type=str,help="ID of the stream")
  parser.add_argument('-c','--choices',nargs="*",help="Choices available in the poll. Defaults to all Operators. Choices are fuzzy matched to hopefully mitigate typos.")
  args = parser.parse_args()
  poll_manager(args)
