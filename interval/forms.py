# -*- encoding: utf-8 -*-

from django.utils.safestring import mark_safe
from django.conf import settings
from django.forms.util import ValidationError
from django.utils.translation import ugettext as _
from datetime import timedelta


ENABLE_DOJANGO = False
if 'dojango' in settings.INSTALLED_APPS:
    ENABLE_DOJANGO = True
    
if ENABLE_DOJANGO:
    from dojango.forms.widgets import TextInput
    from dojango.forms import Field
else:
    from django.forms.widgets import TextInput
    from django.forms import Field



class IntervalWidget(TextInput):

    def __init__(self, format = 'DHMS', *args, **kw):
        TextInput.__init__(self, *args, **kw)
        self.format = format


    def render(self, name, value, attrs=None):
        if value is None:
            days, hours, minutes, seconds = ('0', '0', '0', '0')
        else:
            days = value.days
            hours = value.seconds // 3600
            minutes = (value.seconds - (3600 * hours)) // 60
            seconds = value.seconds - (3600 * hours) - (60 * minutes)

        attrs = self.build_attrs(attrs)

        ret = []
        para = dict(name = name, style = 'style="width: 60px; align: right;"',
                days = days, hours = hours, minutes = minutes, seconds = seconds,
                dojoType = '', days_label = _('days'), hours_label = _('hours'),
                minutes_label = _('minutes'), seconds_label = _('seconds'))
                
        if ENABLE_DOJANGO:
            para['dojoType'] = 'dojoType="dijit.form.NumberTextBox"'

        if "D" in self.format:
            ret.append(u'''<input type="text" value="%(days)s" name="%(name)s_days" %(style)s %(dojoType)s/> %(days_label)s ''')
            

        if "H" in self.format:
            ret.append(u'<input type="text" value="%(hours)s" name="%(name)s_hours" %(style)s %(dojoType) /> %(hours_label)s')


        if "M" in self.format:
            ret.append(u'<input type="text" value="%(minutes)s" name="%(name)s_minutes" %(style)s %(dojoType) /> %(minutes_label)s')

        if "S" in self.format:
            ret.append(u'<input type="text" value="%(seconds)s" name="%(name)s_seconds" %(style)s %(dojoType) /> %(seconds_label)s')
            

        return mark_safe("  ".join(ret) % para)

    
    def value_from_datadict(self, data, files, name):
        kw = dict()
        
        # We get many data in the request: field_name_days, field_name_minutes,
        # and so on. It depends on what is the letter in self.format variable:
        # D(ays), H(ours), M(inutes), S(econds):

        for par in ('days', 'hours', 'minutes', 'seconds'):
            if par[0].upper() in self.format:
                # If this value is in self.format AND the user entered this value
                # we will use it:
                try:
                    kw[par] = int(data.get(name + "_" + par))
                except (TypeError, KeyError, ValueError):
                    # ... but if the value is empty AND this is a required
                    # field, we return None
                    return None
            
        return timedelta(**kw)

    
if ENABLE_DOJANGO:
    IntervalWidget.dojo_type = 'dijit.form.NumberTextBox'

    
class IntervalField(Field):
    
    widget = IntervalWidget

    def __init__(self, format, *args, **kw):
        self.format = format
        self.widget = IntervalWidget(format)
        Field.__init__(self, *args, **kw)

    def clean(self, value):
        if self.required:
            if value == None:
                raise ValidationError, self.default_error_messages['required']
        return Field.clean(self, value)
    