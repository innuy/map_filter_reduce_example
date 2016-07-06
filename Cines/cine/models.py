import math
from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime
from numpy import mean


class Cinema(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def roomQuantity(self):
        return Room.objects.filter(cinema=self.pk).count()

    def rooms(self):
        return Room.objects.filter(cinema=self.pk)

    def rooms_serial(self):
        return Room.objects.filter(cinema=self.pk).values()

    def movies(self):
        list = set()
        a = Room.objects.filter(cinema_id=self.pk)
        for x in a:
            for y in x.roomMovies():
                list.add(y)
        return list

    def freeTime(self):
        a = self.myCinema.all()
        aux = 0
        for x in a:
            aux += x.totalFreeTime()
        hours = aux//3600
        minutes = (aux % 3600) // 60
        seconds = (aux % 60)
        return str(hours)+":"+str(minutes)+":"+str(seconds)

    class Meta:
        managed = True
        db_table = 'cinema'


class Actor(models.Model):
    name = models.CharField(max_length=200)
    birth_date = models.DateField('Birth_date')
    def __str__(self):
        return self.name

    def getShortMovies(self):
        return map(str, map(Movie.getName, filter(lambda d: d.duration_mins < 60, self.movie_set.all())))

    def getLongMovies(self):
        return map(str, map(Movie.getName, filter(lambda d: d.duration_mins > 60, self.movie_set.all())))

    def getMeanShortMovieDuration(self):
        movies = filter(lambda d: d.duration_mins < 60, self.movie_set.all())
        if movies:
            return reduce(mean, map(Movie.getDuration, movies))
        else:
            return "No short movies"

    def getMaxMovieDuration(self):
        movies = self.movie_set.all()
        if movies:
            return reduce(max, map(Movie.getDuration, movies))
        else:
            return "No movies"

    def getMinMovieDuration(self):
        movies = self.movie_set.all()
        if movies:
            return reduce(min, map(Movie.getDuration, movies))
        else:
            return "No movies"

    class Meta:
        managed = True
        db_table = 'actor'

class Movie(models.Model):
    name = models.CharField(max_length=200)
    main_actor = models.ForeignKey(Actor, related_name='main_actor')
    actor = models.ManyToManyField(Actor)
    duration_mins = models.IntegerField()

    def __str__(self):
        return self.name

    def getName(self):
        return self.name

    def getDuration(self):
        return self.duration_mins

    def actors(self):  # Exception!
        return self.actors.all().values()

    def timesPlayed(self):
        return MovieByRoom.objects.filter(movie=self.pk).count()

    def nextReproduction(self):
        items = set()
        for x in Room.objects.all():
            a = MovieByRoom.objects.filter(start_datetime__gt=timezone.now(), room=x.id,
                                           movie=self.pk).order_by('Start_datetime')
            if a.__len__() >= 1:
                items.add(a[0].pk)
        return MovieByRoom.objects.filter(pk__in=items)

    def nextReproduction_serial(self):
        items = set()
        for x in Room.objects.all():
            a = MovieByRoom.objects.filter(start_datetime__gt=timezone.now(), room=x.id,
                                           movie=self.pk).order_by('Start_datetime')
            if a.__len__() >= 1:
                items.add(a[0].pk)
        return MovieByRoom.objects.filter(pk__in=items).values()

    def reproductionTime(self):
        list = set()
        for y in Room.objects.all():
            time = timezone.now() - timezone.now()
            for x in MovieByRoom.objects.filter(movie=self.pk, room=y.pk):
                time = time + (x.end_datetime - x.start_datetime)
            list.add(str(y) + " time: " + str(time))
        return list

    class Meta:
        managed = True
        db_table = 'movie'


class Room(models.Model):
    room_number = models.IntegerField()
    room_manager = models.CharField(max_length=200)
    cinema = models.ForeignKey(Cinema, related_name='myCinema')
    played = models.ManyToManyField(Movie, through='MovieByRoom')

    def __str__(self):
        return self.cinema.name + " " + str(self.room_number)

    def state(self):
        if bool(MovieByRoom.objects.filter(start_datetime__lte=timezone.now(),
                                           end_datetime__gte=timezone.now(), room=self.pk).count()):
            return "Reproducing"
        else:
            return "Inactive"

    def history(self):
        return MovieByRoom.objects.filter(end_datetime__lte=timezone.now(), room=self.pk).distinct()

    def movieQuantity(self):
        q = MovieByRoom.objects.filter(room=self.pk)
        q.query.group_by = ['movie_id']
        return q.count()

    def freeTimeInterval(self):
        list = set()
        a = MovieByRoom.objects.filter(room=self.pk, start_datetime__range=(timezone.now().date(),
                                                                                 timezone.now().date() + timedelta(
                                                                                         days=1))).order_by('Start_datetime')
        b = MovieByRoom.objects.filter(room=self.pk, end_datetime__range=(timezone.now().date(),
                                                                              timezone.now().date() + timedelta(
                                                                                         days=1))).order_by('Start_datetime')
        if len(b) >= 1:
            b = b[0]
            if datetime.combine(b.start_datetime.date(), b.start_datetime.time())  <= datetime.combine(timezone.now().date(), datetime.min.time()):
                init = b.end_datetime
            else:
                init = datetime.combine(timezone.now().date(), datetime.min.time())
        else:
            init = datetime.combine(timezone.now().date(), datetime.min.time())
        for x in a:
            list.add((init.time(), (x.fecha_y_hora_inicio).time()))
            init = x.end_datetime
        if datetime.combine(init.date(), init.time()) <= datetime.combine(timezone.now().date(), datetime.max.time()):
            list.add((init.time(), datetime.min.time().replace(hour = 23, minute = 59, second = 59)))
        return list

    def freeTimeToString(self):
        a = self.freeTimeInterval()
        list = []
        for x in a:
            list.extend(["from: " + str(x[0]) + " to " + str(x[1])])
        return list

    def freePercentage(self):
        hours = 0
        for x in self.freeTimeInterval():
            hours = hours + ((x[1].hour*60*60 + x[1].minute*60 + x[1].second) - (x[0].hour*60*60 + x[0].minute*60 + x[0].second))
        return str("Free: " + str(math.ceil(hours / 864)) + "% and busy: " + str(100 - math.ceil(hours / 864)) + "%")

    def totalFreeTime(self):
        seconds = 0
        for x in self.freeTimeInterval():
            seconds = seconds + ((x[1].hour*60*60 + x[1].minute*60 + x[1].second) - (x[0].hour*60*60 + x[0].minute*60 + x[0].second))
        return seconds

    def roomMovies(self):
        list = set()
        b = MovieByRoom.objects.filter(room=self.pk)
        b.query.group_by = ['movie_id']
        for x in b:
            a = Movie.objects.filter(id=x.movie_id)
            if a.__len__() >= 1:
                list.add(a[0])
        return list

    def playing(self):
        return self.played.values()

    class Meta:
        managed = True
        db_table = 'room'


class MovieByRoom(models.Model):
    movie = models.ForeignKey(Movie)
    room = models.ForeignKey(Room)
    start_datetime = models.DateTimeField('Start_datetime')
    end_datetime = models.DateTimeField('')

    def __str__(self):
        return self.movie.name + " / " + str(self.room) + " / " + str(self.start_datetime)

    def room_serial(self):
        return self.room.objects.values()


def cinemaRoomQuantity():
    list = set()
    for x in Cinema.objects.all():
        list.add(str(x) + " rooms: " + str(x.roomQuantity()))
    return list

def roomState():
    list = set()
    for x in Room.objects.all():
        list.add(str(x) + ", state: " + x.state())
    return list

def roomHistory():
    list = set()
    a = Room.objects.all()
    for x in a:
        for y in x.history():
            list.add(str(x) + " " + y.movie.name)
    return list


class General(models.Model):
    def roomQuantityCinema(self):
        list = set()
        for x in Cinema.objects.all():
            list.add(str(x) + " rooms: " + str(x.roomQuantity()))
        return list

    def roomState(self):
        list = set()
        for x in Room.objects.all():
            list.add(str(x) + ", state: " + x.state())
        return list

    def roomHistory(self):
        list = set()
        a = Room.objects.all()
        for x in a:
            for y in x.history():
                list.add(str(x) + " " + y.movie.name)
        return list
    def actors(self):
        return Actor.objects.all().values("name")