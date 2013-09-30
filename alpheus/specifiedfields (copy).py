from tastypie.resources import ModelResource


class SpecifiedFields(ModelResource):

    def build_filters(self, filters=None):
        self.filters = filters
        return super(SpecifiedFields, self).build_filters(filters)

    def get_object_list(self, request):
    
        self.specified_fields = []
        
        objects = super(SpecifiedFields, self).get_object_list(request)

        distinct = request.GET.get('distinct', False) == 'true'
        fields = request.GET.get("fields", False)
        
        if not fields:
            return objects
        
        
        try:    
            self.specified_fields = fields.split(',')
        except:
            self.specified_fields.append(fields)


        # 
        has_m2m = False
        for field in self.filters:
            try:
                related = objects.model._meta.get_field_by_name(field)[0]
            except:
                related = False
            if related and related.get_internal_type() == 'ManyToManyField':
                has_m2m = True

        only_fields = []
        select_related = []
        self.prefetch_related = []
        
        for specified_field in self.specified_fields:
        
            try:
                fields = specified_field.split('__')
            except:
                continue
        
            # Only adds fields that exist for this model
            # excluding model methods
            for meta_field in objects.model._meta.fields:
            
                if meta_field.name == fields[0]:
                
                    only_fields.append(specified_field)

            # Set `select_related` and `prefetch_related` for related fields
            if len(fields) > 1:
                try:
                    related = objects.model._meta.get_field_by_name(fields[0])[0]
                except:
                    related = False
                    
                if related:
                
                    if related.get_internal_type() == 'ManyToManyField':
                    
                        self.prefetch_related.append(fields[0])
                        
                    elif related.get_internal_type() == 'ForeignKey':
                    
                        select_related.append(fields[0])
        
        
        if len(only_fields): 
            objects = objects.only(*only_fields)
            
        if len(self._meta.excludes):       
            objects = objects.defer(*self._meta.excludes)

        if len(self.prefetch_related):
            objects = objects.prefetch_related(*self.prefetch_related)
            
        if len(select_related):
            objects = objects.select_related(*select_related)

        if (has_m2m and not distinct) or distinct:
            objects = objects.distinct()

        #assert False
        return objects

    def full_dehydrate(self, bundle, for_list=False):
    
        """
        This override disables `full=True` and other things we don't use
        """
        
        if not len(self.specified_fields):
            return super(SpecifiedFields, self).full_dehydrate(self, \
                                                        bundle, for_list)
        
        # Dehydrate each field supplied in the `fields` parameter
        for field_name, field_object in self.fields.items():

            # A touch leaky but it makes URI resolution work.
            if getattr(field_object, 'dehydrated_type', None) == 'related':
                field_object.api_name = self._meta.api_name
                field_object.resource_name = self._meta.resource_name

            # Check for an optional method to do further dehydration.
            method = getattr(self, "dehydrate_%s" % field_name, None)

            if method:
                bundle.data[field_name] = method(bundle)

        bundle = self.dehydrate(bundle)
        return bundle

    def dehydrate(self, bundle):

        # Dehydrate each field including related ones
        for row in self.specified_fields:
        
            f = row.split('__')
            
            if len(f) == 1:
                try:
                    bundle.data[row] = getattr(bundle.obj, f[0])()
                except:
                    bundle.data[row] = getattr(bundle.obj, f[0])
            elif len(f) == 2:

                try:
                    for m2m in getattr(bundle.obj, f[0]).all():
                        if m2m.pk == bundle.obj.id:
                            if f[0] not in bundle.data:
                                bundle.data[f[0]] = {}
                            bundle.data[f[0]][f[1]] = getattr(m2m, f[1])
                    
                    #bundle.obj.author.get(book=bundle.obj.id).first_name
                    #bundle.data[row] = getattr(getattr(bundle.obj, fields[0]).get(**kwargs), fields[1])
                except:
                    try:
                        bundle.data[row] = getattr(getattr(bundle.obj, f[0]), f[1])
                        #bundle.data[fields[0]] = bundle.obj
                    except:
                        pass  
                        
            elif len(f) == 3:
                try:
                    for m2m in getattr(bundle.obj, f[0]).all():
                        if m2m.pk == bundle.obj.id:
                            if f[0] not in bundle.data:
                                bundle.data[f[0]] = {}
                            bundle.data[f[0]][f[1]] = getattr(m2m, f[1])
                except:
                    try:
                        
                        bundle.data[row] = getattr(getattr(getattr(bundle.obj, \
                                                            f[0]), f[1]), f[2])
                    except:
                        raise Exception("'%s' not found." % row)   
                                      
            #bundle.data[row] = reduce(getattr, fields, bundle.obj)
            
            # display actual values for `choices` fields
            method = getattr(bundle.obj, "get_%s_display" % f[0], False)
            if method:
                bundle.data[f[0]] = method()
        return bundle

            

