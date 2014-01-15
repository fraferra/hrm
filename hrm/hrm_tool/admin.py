from django.contrib import admin
from hrm_tool.models import *
from django.contrib.auth.models import User


class BusinessUnitAdmin(admin.ModelAdmin):
	model=BusinessUnit

	fieldsets=[
       ('Info',{'fields':['unit']})
	]


admin.site.register(BusinessUnit, BusinessUnitAdmin)


class EmployeeAdmin(admin.ModelAdmin):
	model=Employee

	fieldsets=[
       ('Info',{'fields':['user','first_name','last_name','business_unit','superior']}),
       ('Skills',{'fields':['skill_1','skill_level_1','skill_2','skill_level_2','skill_3','skill_level_3']}),
	]

	def first_name(self, instance):
		return instance.user.first_name
	def last_name(self, instance):
		return instance.user.last_name
	def business_unit(self, instance):
		return instance.user.business_unit

admin.site.register(Employee, EmployeeAdmin)

class ManagerAdmin(admin.ModelAdmin):
	model=Manager

	fieldsets=[
       ('Info',{'fields':['user','first_name','last_name','business_unit','superior']})
	]

	def first_name(self, instance):
		return instance.user.first_name
	def last_name(self, instance):
		return instance.user.last_name
	def business_unit(self, instance):
		return instance.user.business_unit

admin.site.register(Manager, ManagerAdmin)

class SeniorManagerAdmin(admin.ModelAdmin):
	model=SeniorManager

	fieldsets=[
       ('Info',{'fields':['user','first_name','last_name','business_unit','superior']}),

	]

	def first_name(self, instance):
		return instance.user.first_name
	def last_name(self, instance):
		return instance.user.last_name
	def business_unit(self, instance):
		return instance.user.business_unit

admin.site.register(SeniorManager, SeniorManagerAdmin)

class SeniorVicePresidentAdmin(admin.ModelAdmin):
	model=SeniorVicePresident

	fieldsets=[
       ('Info',{'fields':['user','first_name','last_name','business_unit','office']})
	]

	def first_name(self, instance):
		return instance.user.first_name
	def last_name(self, instance):
		return instance.user.last_name
	def business_unit(self, instance):
		return instance.user.business_unit

admin.site.register(SeniorVicePresident, SeniorVicePresidentAdmin)