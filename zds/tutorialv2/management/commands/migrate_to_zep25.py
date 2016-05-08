# coding: utf-8

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_text
from django.utils.text import slugify

from zds import settings
from zds.tutorialv2.models.models_database import PublishableContent
from zds.utils.models import Category, SubCategory, CategorySubCategory, Tag
from zds.utils.mps import send_mp


def categories_to_tags():
    """
    Change all content categories to tags.

    :return: None
    """
    n = 0
    contents = PublishableContent.objects.all()
    for content in contents:
        categories = content.subcategory.all()
        for cat in categories:
            tag_title = smart_text(cat.slug.replace('-', ' ').strip().lower())
            current_tag = Tag.objects.filter(title=tag_title).first()
            if current_tag is None:
                current_tag = Tag(title=tag_title)
                current_tag.save()
                print('[ZEP-25] : Tag "{}" added'.format(current_tag))
                n += 1
            # do not add "autre" tag (useless)
            if current_tag != 'autre':
                content.tags.add(current_tag)
        content.save()
    print('[ZEP-25] : {} new tag(s)'.format(n))


def update_categories():
    """
    Delete all categories and create new ones.

    :return: None
    """
    for cat in SubCategory.objects.all():
        print('[ZEP-25] : Old category "{}" deleted'.format(cat))
        cat.delete()
    for cat in Category.objects.all():
        print('[ZEP-25] : Old subcategory "{}" deleted'.format(cat))
        cat.delete()
    for cat in CategorySubCategory.objects.all():
        cat.delete()
    print('[ZEP-25] : Categories and subcatagories deleted')
    categories = ['Informatique', 'Sciences de la nature', 'Sciences humaines et sociales', 'Autres']
    subcategories = [
        # Informatique
        [
            ('Bureautique et rédaction', 'Excel, LaTeX, Powerpoint, Word'),
            ('Matériel et électronique', 'Arduino, Disque dur, DIY, Electronique*, Mémoires, Ordinateur'),
            ('Programmation et algorithmique', '.NET, Ada, Algorithmique, C, C#, C++, Cobol, Fonctionnel, Génie logicie'
                                               'l, Haskell, Java, Julia, Lisp, Ocaml, Orienté objet, Python, Ruby, Vers'
                                               'ioning'),
            ('Site web', 'Accessibilité, Actionscript, Angular JS, CakePHP, Django, HTML/CSS, Java EE, JavaScript, Ngin'
                         'x, Node.js, Oxygen, PHP, Ruby On Rails, SEO/Réferencement*, Symfony, Websocket'),
            ('Systèmes d\'exploitation', 'Android, GNU/Linux, iOS, MAC OS, Windows, Windows Phone'),
            ('Autres (informatique)', 'API, Base de données, FTP, Jeux vidéos, MySQL, Oracle, Protocole, Sécurité, TCP/'
                                      'IP'),
        ],
        # Sciences de la nature
        [
            ('Astronomie', 'Astronomie'),
            ('Géologie et géographie physique', 'Géologie'),
            ('Biologie', 'Biologie'),
            ('Physique', 'Physique'),
            ('Chimie', 'Chimie'),
            ('Mathématiques', 'Mathématiques'),
            ('Autres (sciences de la nature)', 'Autres sciences de la nature')
        ],
        # Sciences humaines et sociales
        [
            ('Droit', 'Droit'),
            ('Histoire', 'Histoire'),
            ('Langues', 'Langues'),
            ('Psychologie', 'Psychologie, Pédagogie'),
            ('Économie', 'Économie'),
            ('Autres (sciences humaines et sociales)', 'Autres sciences humaines et sociales comme la géographie')
        ],
        # Autres
        [
            ('Arts, graphisme et multimédia', 'Graphisme 2D, Graphisme 3D, Musique, Son'),
            ('Communication et management', 'Monde du travail'),
            ('Zeste de Savoir', 'Zeste de Savoir'),
            ('Autres', 'Littérature, Interview')
        ]
    ]
    i = 0
    for category in categories:
        cat = Category()
        cat.title = category
        cat.description = category
        cat.position = i
        cat.slug = slugify(u'{}'.format(category))
        cat.save()
        print('[ZEP-25] : New category "{}" added'.format(cat))
        for subcategory in subcategories[i]:
            sub = SubCategory()
            sub.title = subcategory[0]
            sub.subtitle = subcategory[1]
            sub.slug = slugify(u'{}'.format(subcategory[0]))
            sub.save()
            print('[ZEP-25] : New subcategory "{}" added'.format(sub))
            catsubcat = CategorySubCategory()
            catsubcat.category = cat
            catsubcat.subcategory = sub
            catsubcat.save()
            print('[ZEP-25] : Relation "{}" <--> "{}" added'.format(cat, sub))
        i += 1


def alert_authors():
    """
    Send a private message to all authors (with a `PublishableContent`) for new tags system.

    :return: None
    """
    bot = get_object_or_404(User, username=settings.ZDS_APP['member']['bot_account'])
    bots = [
        get_object_or_404(User, username=settings.ZDS_APP['member']['bot_account']),
        get_object_or_404(User, username=settings.ZDS_APP['member']['anonymous_account']),
        get_object_or_404(User, username=settings.ZDS_APP['member']['external_account'])
    ]
    users = []
    contents = PublishableContent.objects.all()
    for content in contents:
        authors = content.authors.all()
        for author in authors:
            if author not in users and author not in bots:
                users.append(author)
    for user in users:
        msg = 'Bonjour,\n\nDepuis la dernière version de Zeste de Savoir, tous les contenus (articles, tutoriels ' \
              'et bientôt tribunes libres) possèdent maintenant une nouvelle classification ([ZEP-25](https://zestede' \
              'savoir.com/forums/sujet/2378/zep-25-categorisation-des-articles-et-tutoriels/)). Les **tags** ont fait' \
              ' leur apparition et les catégories ont été revues afin de faciliter et d\'aléger cette classification.' \
              '\n\nLes anciennes catégories ont été transformées en tags et de nouvelles catégories plus générales on' \
              't été ajoutés. L\'équipe de Zeste de Savoir va ou a déjà changé les catégories des contenus publiés.\n' \
              '\nNous vous invitons à vérifier la catégorie de vos [articles](https://zestedesavoir.com/contenus/arti' \
              'cles/{1}/) et [tutoriels](https://zestedesavoir.com/contenus/tutoriels/{1}/) mais également la pertine' \
              'nce des tags et en ajouter si besoin.\n\n\nNous restons à votre disposition et votre écoute pour toute' \
              's suggestions ou remarques,\n\nL\'équipe de Zeste de Savoir'
        send_mp(
            bot,
            [user],
            'Changement de classification du contenu sur Zeste de Savoir',
            'Ce qui change pour vous en tant qu\'auteur',
            msg
        )
        print('[ZEP-25] : PM send to {}'.format(user))


def migrate_zds():
    """
    Migrate online content of ZdS based on pk.

    :return: None
    """
    sucess = 0
    fail = 0
    missing = 0
    # LAST UPDATE : 20/03/2016 10:30
    contents = {
        # Informatique
        'Bureautique et rédaction': [244, 409, 439, 508, 601, 602, 630],
        'Matériel et électronique': [
            253, 255, 264, 279, 343, 349, 364, 365, 371, 374, 428, 429, 507, 599, 613, 640, 686, 749, 757, 895, 917,
            1116],
        'Programmation et algorithmique': [5, 28, 30, 39, 43, 54, 56, 60, 61, 65, 66, 67, 78, 96, 100, 152, 158, 159,
                                           160, 164, 175, 209, 223, 247, 248, 260, 262, 272, 274, 281, 292, 309, 312,
                                           315, 325, 331, 334, 427, 460, 461, 476, 484, 496, 528, 531, 553, 558, 574,
                                           582, 591, 597, 609, 612, 621, 624, 634, 644, 645, 646, 674, 681, 685, 706,
                                           723, 755, 799, 839, 870, 884, 912, 945, 954, 962],
        'Site Web': [57, 193, 232, 241, 246, 248, 292, 295, 312, 344, 351, 352, 358, 411, 446, 449, 449, 527, 574, 591,
                     597, 598, 599, 612, 620, 622, 925, 945],
        'Systèmes d’exploitation': [37, 39, 97, 100, 130, 143, 158, 268, 317, 357, 507, 607, 624, 609, 662, 683],
        'Autres (informatique)': [4, 12, 88, 193, 245, 250, 297, 299, 321, 323, 324, 351, 379, 415, 723, 730, 925],
        # Sciences de la nature
        'Astronomie': [63, 85, 102, 105, 378, 408],
        'Géologie et géographie physique': [169, 378, 403, 404, 405, 408, 526],
        'Biologie': [105, 148, 157, 223, 410, 451, 493],
        'Physique': [74, 148, 164, 279, 381, 428, 614, 895, 1052],
        'Chimie': [73, 166, 253, 569],
        'Mathématiques': [27, 43, 54, 65, 66, 67, 160, 244, 281, 329, 484, 528, 596, 676, 735, 803, 810, 829, 1184],
        'Autres (sciences de la nature)': [44],
        # Sciences humaines et sociales
        'Droit': [59, 261, 444],
        'Histoire': [12, 54, 65, 66, 155, 183, 381, 614, 676],
        'Langues': [155, 162, 376, 452, 748],
        'Psychologie': [4, 163, 171, 305, 352, 410, 421, 479, 488, 604, 793],
        'Économie': [197, 500],
        'Autres (sciences humaines et sociales)': [127],
        # Autres
        'Arts, graphisme et multimédia': [151, 153, 212, 251, 334, 599, 626, 655, 656, 671, 706, 751, 913],
        'Communication et management': [305, 341, 391],
        'Zeste de Savoir': [1, 8, 9, 11, 13, 14, 15, 20, 22, 36, 38, 40, 48, 49, 52, 59, 64, 71, 72, 77, 82, 83, 86, 90,
                            93, 99, 108, 115, 137, 138, 142, 145, 173, 174, 185, 194, 195, 196, 198, 206, 216, 222, 244,
                            249, 261, 877, 978, 1002, 1120, 1162, ],
        'Autres': [11, 13, 14, 15, 52, 69, 90, 95, 103, 104, 142, 173, 196, 195, 936, 950, 1139],
    }
    contents_pk = [item['pk'] for item in PublishableContent.objects.values('pk')]
    for subcat, cts in contents.items():
        for ct in cts:
            try:
                content = PublishableContent.objects.get(pk=ct)
                subcategory = SubCategory.objects.get(title=subcat)
                content.subcategory.add(subcategory.pk)
                content.save()
                try:
                    contents_pk.remove(ct)
                except ValueError:
                    # contents with more than one category
                    pass
                print('[ZEP-25] : New category "{}" for content "{}"'.format(subcategory, content))
                sucess += 1
            except PublishableContent.DoesNotExist:
                print('[ZEP-25][WARNING] : Content with pk "{}" is not in list, it should not happend in production'
                      .format(ct))
                fail += 1

    # alert for content not in list
    for pk in contents_pk:
        content = PublishableContent.objects.get(pk=pk)
        print('[ZEP-25][WARNING] : Content "{}" (pk = {}) is not migrate (not in list), please check it'.format(content,
                                                                                                                pk))
        missing += 1

    # migration details
    print('\n================================================================================\n')
    print('{} content(s) migrated with succes'.format(sucess))
    print('{} content(s) failed'.format(fail))
    print('{} content(s) unmigrated'.format(missing))
    if fail != 0 or missing != 0:
        print('\nPLEASE CHECKS LOGS.')
    print('\n================================================================================\n')


@transaction.atomic
class Command(BaseCommand):
    help = 'Change all content categories to tags (ZEP-25).\n\n\nOptions:\n\n  No options run all commands (except he' \
           'lp) in this order : tags, categories, alert, prod\n\n  alert         Send a private message to all author' \
           's for new tags system\n  categories    Delete all categories and create new ones\n  help          Show th' \
           'is message\n  prod          Convert all published content in https://zestedesavoir.com\n  tags          C' \
           'hange all content categories to tags'

    def handle(self, *args, **options):
        if len(args) > 0:
            if args[0] == 'alert':
                alert_authors()
            elif args[0] == 'categories':
                update_categories()
            elif args[0] == 'help':
                print(self.help)
            elif args[0] == 'tags':
                categories_to_tags()
            elif args[0] == 'prod':
                migrate_zds()
            else:
                print('Unknow option.')
                print(self.help)
        else:
            categories_to_tags()
            update_categories()
            alert_authors()
            migrate_zds()
