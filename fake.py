import os
import itertools
import datetime
import pytz
from random import randint, shuffle, sample
from abc import ABC, abstractmethod

from faker import Faker
from faker.providers import internet

import django


try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NTUSport.settings")
    django.setup()
finally:
    from django.contrib.auth.models import User, Group
    from django.db.models import Q
    from django.db import transaction
    from player.models import Student
    from player.departments import Department
    from team.models import Team
    from schedule.models import Schedule, Competition, Statistic


class ModelFaker(ABC):
    def __init__(self):
        self.faker = Faker('zh_TW')

    @abstractmethod
    def fake(self):
        pass


class StudentFaker(ModelFaker):
    def fake(self, num=10, depart=None):
        student_group = Group.objects.get(name='Student')
        for _ in range(num):
            with transaction.atomic():
                fake_profile = self.faker.profile(
                    fields=['username', 'mail'])
                user = User.objects.create_user(
                    fake_profile['username'],
                    fake_profile['mail'],
                    '1234567890'
                )
                user.last_name = self.faker.last_name()
                user.first_name = self.faker.first_name()
                student_group.user_set.add(user)
                if depart:
                    student = Student.objects.create(
                        user=user,
                        student_id='B'+''.join(str(randint(0, 9))
                                               for _i in range(8)),
                        department=depart,
                        grade=randint(1, 6),
                    )
                else:
                    num_choice = len(Department.DEPARTMENT_CHOICE)
                    rand_choice = randint(0, num_choice-1)
                    student = Student.objects.create(
                        user=user,
                        student_id='B'+''.join(str(randint(0, 9))
                                               for _i in range(8)),
                        department=Department.DEPARTMENT_CHOICE[rand_choice][0],
                        grade=randint(1, 6),
                    )
                user.save()
                student.save()
        student_group.save()


class TeamFaker(ModelFaker):
    def fake(self):
        for department in Department.DEPARTMENT_CHOICE:
            with transaction.atomic():
                department = department[0]
                students = Student.objects.filter(department=department)
                if not students:
                    StudentFaker().fake(depart=department)
                    students = Student.objects.filter(department=department)
                team, created = Team.objects.get_or_create(
                    department=department,
                    defaults={
                        'caption': students.first(),
                    }
                )
                team.players.set(students)
                team.save()


class ScheduleFaker(ModelFaker):
    def fake(self, num=10):
        teams = Team.objects.all()
        comb = list(itertools.combinations(teams, 2))
        shuffle(comb)

        for i, team_set in enumerate(comb):
            if i >= num:
                break
            with transaction.atomic():
                schedule = Schedule.objects.create(
                    date=self.faker.date_time_ad(
                        tzinfo=pytz.timezone('Asia/Taipei'),
                        start_datetime=datetime.datetime.now()
                    )
                )
                referees = Student.objects.exclude(
                    Q(department=team_set[0].department) |
                    Q(department=team_set[1].department))
                for team in team_set:
                    Competition.objects.create(
                        team=team,
                        schedule=schedule
                    )

                schedule.referees.set(referees[:2])
                schedule.save()


class StatisticFaker(ModelFaker):
    def fake(self, competition, num=10):
        with transaction.atomic():
            if competition.players.count() == 0:
                join_players = sample(set(competition.team.players.all()),
                                      randint(0, competition.team.players.count()))

                for player in join_players:
                    fga = randint(0, 10)
                    three_pa = randint(0, 10)
                    fta = randint(0, 10)
                    Statistic.objects.create(
                        competition=competition,
                        player=player,
                        MIN=randint(0, 48),
                        PTS=randint(0, 20),
                        FGA=fga,
                        FGM=randint(0, fga),
                        three_PA=three_pa,
                        three_PM=randint(0, three_pa),
                        FTA=fta,
                        FTM=randint(0, fta),
                        OR=randint(0, 10),
                        DR=randint(0, 10),
                        BS=randint(0, 3),
                        AST=randint(0, 5),
                        BLK=randint(0, 10),
                        STL=randint(0, 10),
                        TO=randint(0, 30)
                    )


if __name__ == '__main__':
    # StudentFaker().fake(num=50)
    # TeamFaker().fake()
    # ScheduleFaker().fake()

    f = StatisticFaker()
    for comp in Competition.objects.all():
        f.fake(comp)
