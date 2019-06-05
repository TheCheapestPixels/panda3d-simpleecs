import simpleecs


@simpleecs.Component('LIVING')
class Living:
    pass


@simpleecs.Component('AGE')
class Age:
    age: float


class AgingSystem:
    # Each time manager.update() is called, the system's methods are called;
    # * init_components() with any newly created component (of a type listed),
    # * destroy() with those that should be removed (of a type listed),
    # * update() with any remaining existing components (of a type listed).
    # Thus, for purposes of selecting the entities on which to run this system,
    # this is an OR filter. It returns *any* matching component, not just those
    # of entities having *all* listed components.
    # Do note that when a system is added to the manager, it does not get to
    # process already existing components with init_components().
    component_types = [
        'LIVING',
        'AGE',
    ]

    def init_components(self, components):
        pass

    def destroy_components(self, components):
        for living in components['LIVING']:
            # This entity just died of old age. Decide here whether to make
            # dead or undead.
            print("  Character dies of old age")

    def update(self, dt, components):
        print("  update() processes: "+str(components))
        for age in components['AGE']:
            age.age += dt
            print("  Character age is now {}".format(age.age))
            if age.age >= 5 and age.entity.has_component('LIVING'):
                print("  Character now will die of old age")
                # After removing the entity's Living component, this system
                # should not be active anymore for this entity, or rather there
                # should be a way of setting it up so that it is not active
                # anymore. This is not currently the case, so we had to test for
                # that.
                age.entity.remove_component(age.entity.get_component('LIVING'))


manager = simpleecs.ECSManager()
manager.add_system(AgingSystem())
entity = manager.create_entity()
entity.add_component(Living())
entity.add_component(Age(age=0))


for t in range(10):
    # Here we could ask for player action. For example, if alive, they could
    # cast a "should I die, make me a lich" spell, or a "set my age back and
    # revive me" one. Or one that just revives them, just so they can die of old
    # age again right away.
    print("Timestep {}".format(t + 1))
    manager.update(1)
