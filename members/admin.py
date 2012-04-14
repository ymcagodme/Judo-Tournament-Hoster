from django.contrib import admin
from django import forms
from members.models import Member, Mat, Division, Match

class MemberAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'dojo', 'division')
    search_fields = ['last_name', 'first_name', 'dojo']

class DivisionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'gender', 'age', 'weight', 'rank', 'mat')
    search_fields = ['mat', 'gender', 'age', 'weight', 'rank']
    
class MatchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        try:
            match_instance = Match.objects.filter(pk=self.instance.pk)[0]
            competitors = match_instance.competitors.all()
            if(len(competitors) > 0):
                pk_dict = {}
                for m in competitors:
                    pk_dict[m.pk] = m.__unicode__()
                tuple_list = [(0, '------')]
                for key, val in pk_dict.iteritems():
                    tuple_list.append((key, val))
                choices = tuple(tuple_list)
            else:
                choices = ( (0, 'No Competitors'), )
        except IndexError: 
            choices = ( (0, 'No Competitors'), )
        self.fields['winner'] = forms.ChoiceField(choices=choices)

class MatchAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'p1_name', 'p2_name', 'match_is_finished')
    ordering = ['match_number']
    filter_horizontal = ("competitors",)
    form = MatchForm
    def p1_name(self, obj):
        competitors = obj.competitors.all()
        try: return competitors[0]
        except IndexError: return "N/A"
    p1_name.short_description = 'Competitor #1'
    def p2_name(self, obj):
        competitors = obj.competitors.all()
        try: return competitors[1]
        except IndexError: return "N/A"
    p2_name.short_description = 'Competitor #2'
    def match_is_finished(self, obj):
        if obj.winner == 0:
            return False
        return True
    match_is_finished.boolean = True

admin.site.register(Member, MemberAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Mat)
