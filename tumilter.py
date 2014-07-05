
import Milter
import string

recipients = 2	# define maximum number of recipients int To an Cc here
socketname = "/tmp/tumilter"

class TuMilter(Milter.Milter):
  "Milter to limit the numer of To and Cc recipients"

  def __init__(self):
    self.tocc = 0

  def header(self,name,val):

    sv = self.getsymval('{auth_authen}')
    if sv==None or sv=="":
      return Milter.CONTINUE

    lname = name.lower()
    if lname == 'to' or lname=='cc':
      mails = string.split(val, ',')
      self.tocc=self.tocc+len(mails)

    if self.tocc >= recipients:
      self.setreply('550',None,'Sorry, your message has too many recipients')
      return Milter.REJECT
   
    return Milter.CONTINUE
    

if __name__ == "__main__":
  Milter.factory = TuMilter
  Milter.runmilter("tumilter",socketname,240)
