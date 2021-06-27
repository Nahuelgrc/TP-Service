from datetime import datetime

class ToDict():
  def to_dict(self):

    return {
      col.name: Converter.datetimeToString(getattr(self, col.name)) if type(getattr(self, col.name)) == datetime else getattr(self, col.name)
      for col in self.__table__.columns  
    }
    #return { col.name: getattr(self, col.name) for col in self.__table__.columns }

class Converter():
  @staticmethod
  def stringToDatetime(datetime_string):
    return datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")

  @staticmethod
  def datetimeToString(datetime:datetime):
    return datetime.strftime("%Y-%m-%d %H:%M:%S")