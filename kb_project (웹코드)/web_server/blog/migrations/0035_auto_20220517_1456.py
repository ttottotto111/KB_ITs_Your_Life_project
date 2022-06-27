# Generated by Django 3.2 on 2022-05-17 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0034_alter_post_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='title',
            new_name='차종',
        ),
        migrations.AddField(
            model_name='post',
            name='브랜드',
            field=models.CharField(blank=True, choices=[('현대', '현대'), ('기아', '기아'), ('쉐보레', '쉐보레'), ('르노삼성', '르노삼성'), ('쌍용', '쌍용'), ('제네시스', '제네시스'), ('BMW', 'BMW'), ('벤츠', '벤츠'), ('아우디', '아우디'), ('폭스바겐', '폭스바겐'), ('미니', '미니'), ('지프', '지프'), ('포드', '포드'), ('볼보', '볼보'), ('랜드로버', '랜드로버'), ('푸조', '푸조'), ('재규어', '재규어'), ('렉서스', '렉서스'), ('링컨', '링컨'), ('인피니티', '인피니티'), ('혼다', '혼다'), ('도요타', '도요타'), ('포르쉐', '포르쉐'), ('닛산', '닛산'), ('캐딜락', '캐딜락'), ('대형트럭(2톤이상)', '대형트럭(2톤이상)'), ('마세라티', '마세라티'), ('시트로엥', '시트로엥'), ('토요타', '토요타'), ('크라이슬러', '크라이슬러'), ('피아트', '피아트'), ('대형버스(16인승이상)', '대형버스(16인승이상)'), ('테슬라', '테슬라'), ('닷지', '닷지'), ('미쯔비시', '미쯔비시'), ('북기은상', '북기은상'), ('스마트', '스마트'), ('벤틀리', '벤틀리'), ('애스턴마틴', '애스턴마틴'), ('롤스로이스', '롤스로이스'), ('선롱', '선롱'), ('람보르기니', '람보르기니'), ('험머', '험머')], max_length=30, null=True),
        ),
    ]
