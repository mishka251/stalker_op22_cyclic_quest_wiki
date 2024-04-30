from game_parser.logic.model_resources.base_resource import SECTION_NAME, BaseModelResource, BooleanField, CharField, DecimalField, IntegerField
from game_parser.models import Addon, Ammo, Artefact, Explosive, Grenade, GrenadeLauncher, Knife, MonsterPart, Other, Outfit, Scope, Silencer, Weapon
from game_parser.models.items.artefact import CapsAnom, MonsterEmbrion, TrueArtefact
from game_parser.models.items.base_item import BaseItem


class BaseItemResource(BaseModelResource):
    _model_cls = BaseItem
    _fields = [
        CharField(SECTION_NAME, "name"),
        CharField("visual", "visual_str"),
        CharField("description", "description_code", required=False, default=""),
        IntegerField("cost"),
        CharField("inv_name", required=False),
        CharField("inv_name_short", required=False),
        DecimalField("inv_weight"),
        BooleanField("cheat_item"),
        BooleanField("quest_item"),
        IntegerField("inv_grid_width"),
        IntegerField("inv_grid_height"),
        IntegerField("inv_grid_x"),
        IntegerField("inv_grid_y"),
    ]


class AddonResource(BaseItemResource):
    _model_cls = Addon


class SilencerResource(AddonResource):
    _model_cls = Silencer
    _fields = [
        *AddonResource._fields,
        DecimalField("condition_shot_dec", required=False),
    ]

    _exclude_fields = {
        *AddonResource._exclude_fields,
        "fire_dispersion_base_k",
        "cam_dispersion_k",
        "ui_show_condition",
        "condition_critical",
        "condition_critical_message",
        "bullet_hit_power_k",
        "bullet_speed_k",
    }


class ScopeResource(AddonResource):
    _model_cls = Scope

    _exclude_fields = {
        *AddonResource._exclude_fields,
        "holder_range_modifier",
        "holder_fov_modifier",
        "scope_texture",
        "scope_zoom_factor",
        "scope_zoom_step_count",
    }


class GrenadeLauncherResource(AddonResource):
    _model_cls = GrenadeLauncher
    _fields = [
        *AddonResource._fields,
        CharField("ammo_class", required=False),
    ]
    _exclude_fields = {
        *AddonResource._exclude_fields,
        "fire_dispersion_base",
        "scope_texture",
        "scope_zoom_factor",
    }


class ExplosiveResource(BaseItemResource):
    _model_cls = Explosive

    _exclude_fields = {
        *BaseItemResource._exclude_fields,
        "blast",
        "blast_r",
        "blast_impulse",
        "frags",
        "frags_r",
        "frag_hit",
        "frag_hit_impulse",
        "hit_type_blast",
        "hit_type_frag",
        "up_throw_factor",
        "wm_size",
        "explode_particles",
        "light_color",
        "light_range",
        "light_time",
        "fragment_speed",
        "explode_duration",
        "snd_explode",
        "immunities_sect",

        "can_take",
        "time_to_explode",
        "snd_checkout",

        "radius",
        "bomba",
        "script_binding",
        "explode_hide_duration",
        "explode_effector_section",
        "mass",
    }


class KnifeResource(BaseItemResource):
    _model_cls = Knife
    _exclude_fields = {
        *BaseItemResource._exclude_fields,
        "holder_range_modifier",
        "holder_fov_modifier",
        "scope_texture",
        "scope_zoom_factor",
        "hit_power",
        "hit_impulse",
        "hit_power_2",
        "hit_impulse_2",
        "fire_distance",
        "condition_shot_dec",
        "critical_condition",
        "snd_shoot",
        "snd_shoot1",
        "snd_shoot2",
        "position",
        "hud",
        "orientation",
        "snd_draw",
        "snd_holster",
        "hit_type",
        "hit_type_2",
        "rpm",
        "sprint_allowed",
    }


class GrenadeResource(BaseItemResource):
    _model_cls = Grenade
    _exclude_fields = {
        *BaseItemResource._exclude_fields,
        "grenade_remove_time",
        "detonation_threshold_hit",
        "script_binding",
        "ef_weapon_type",
        "animation_slot",
        "single_handed",
        "slot",
        "hud",
        "force_min",
        "force_const",
        "force_max",
        "force_grow_speed",
        "destroy_time",
        "blast",
        "blast_r",
        "blast_impulse",
        "frags",
        "frags_r",
        "frag_hit",
        "frag_hit_impulse",
        "hit_type_blast",
        "hit_type_frag",
        "up_throw_factor",
        "explode_particles",
        "light_color",
        "light_range",
        "light_time",
        "fragment_speed",
        "explode_duration",
        "snd_explode",
        "snd_checkout",
        "attach_position_offset",
        "attach_angle_offset",
        "attach_bone_name",
        "throw_point",
        "throw_dir",
        "wm_size",
        "wallmark_section",
        "weapon_type",
        "upgr_icon_x",
        "upgr_icon_y",
        "upgr_icon_width",
        "upgr_icon_height",
        "hide_in_explosion",
        "explode_hide_duration",
        "dynamic_explosion_particles",

        "box_size",
        "k_dist",
        "k_disp",
        "k_hit",
        "k_impulse",
        "k_pierce",
        "impair",
        "buck_shot",
        "tracer",
        "jump_height",
        "fake_grenade_name",

        "condition_to_explode",
        "time_to_explode",
        "set_timer_particles",
        "blowout_light",
        "light_height",

        "ph_mass",
        "snd_fly_sound",
        "engine_present",
        "engine_work_time",
        "engine_impulse",
        "engine_impulse_up",
        "lights_enabled",
        "trail_light_color",
        "trail_light_range",
        "engine_particles",
        "force_explode_time",
        "tracer_color_ID",
        "explosive",
    }


class AmmoResource(BaseItemResource):
    _model_cls = Ammo
    _fields = [
        *BaseItemResource._fields,
        DecimalField("box_size", required=False),
        DecimalField("k_dist", required=False),
        DecimalField("k_disp", required=False),
        DecimalField("k_hit", required=False),
        DecimalField("k_impulse", required=False),
        DecimalField("k_pierce", required=False),
        DecimalField("impair", required=False),
        DecimalField("wm_size", required=False),
        CharField("tracer", "tracer_str", required=False),
        CharField("explosive", "explosive_str", required=False, default="off"),
        DecimalField("buck_shot", required=False),
    ]
    _exclude_fields = {
        *BaseItemResource._exclude_fields,
        "fake_grenade_name",
    }


class WeaponResource(BaseItemResource):
    _model_cls = Weapon

    _fields = [
        *BaseItemResource._fields,
        CharField("ef_main_weapon_type", required=False),
        CharField("ef_weapon_type", required=False),
        CharField("weapon_class", required=False),
        IntegerField("ammo_mag_size"),
        CharField("fire_modes", "fire_modes_str", required=False),
        CharField("ammo_class", "ammo_class_str"),
        CharField("grenade_class", "grenade_class_str", required=False),
        IntegerField("rpm"),
        CharField("scope_status", "scope_status_str"),
        CharField("silencer_status", "silencer_status_str"),
        CharField("grenade_launcher_status", "grenade_launcher_status"),
        CharField("scope_name", required=False),
        CharField("silencer_name", required=False),
        CharField("grenade_launcher_name", required=False),
        IntegerField("ammo_limit", required=False),
        IntegerField("ammo_elapsed", required=False),
        IntegerField("ammo_current", required=False),
        IntegerField("slot", required=False),
    ]

    _exclude_fields = {
        *BaseItemResource._exclude_fields,
        "min_radius",
        "max_radius",
        "holder_range_modifier",
        "holder_fov_modifier",
        "control_inertion_factor",
        "disp_rate",
        "cam_relax_speed",
        "cam_dispersion",
        "cam_dispersion_inc",
        "cam_dispertion_frac",
        "cam_max_angle",
        "cam_max_angle_horz",
        "cam_step_angle_horz",
        "fire_dispersion_condition_factor",
        "misfire_probability",
        "misfire_condition_k",
        "condition_shot_dec",
        "hand_dependence",
        "single_handed",
        "direction",
        "shell_point",
        "fire_point",
        "fire_point2",
        "flame_particles",
        "smoke_particles",
        "PDM_disp_base",
        "PDM_disp_vel_factor",
        "PDM_disp_accel_factor",
        "PDM_crouch",
        "PDM_crouch_no_acc",
        "hud",
        "normal",
        "position",
        "orientation",
        "strap_position",

        "light_color",
        "light_range",
        "light_var_color",
        "light_var_range",
        "light_time",
        "zoom_enabled",
        "scope_zoom_factor",
        "snd_draw",
        "snd_holster",
        "snd_shoot",
        "snd_empty",
        "snd_reload",
        "snd_close",
        "scope_x",
        "scope_y",
        "silencer_x",
        "silencer_y",
        "silencer_smoke_particles",
        "silencer_light_color",
        "silencer_light_range",
        "silencer_light_var_color",
        "silencer_light_var_range",
        "silencer_light_time",
        "snd_shoot1",
        "snd_silncer_shot",
        "bullet_speed",
        "use_aim_bullet",
        "time_to_aim",
        "silencer_hit_power",
        "silencer_hit_impulse",
        "silencer_fire_distance",
        "silencer_bullet_speed",
        "animation_slot",
        "auto_spawn_ammo",
        "dispersion_start",
        "fire_dispersion_base",
        "shell_dir",
        "shell_particles",
        "hit_power",
        "hit_impulse",
        "hit_type",
        "hit_rate",
        "fire_distance",
        "rpm_empty_click",
        "strap_orientation",
        "strap_bone0",
        "strap_bone1",
        "light_disabled",
        "ph_mass",
        "snd_zoomdec",
        "snd_zoominc",
        "tri_state_reload",
        "startup_ammo",
        "snd_shoot_duplet",
        "snd_open_weapon",
        "snd_add_cartridge",
        "snd_close_weapon",
        "snd_shoot2",
        "snd_shoot3",
        "grenade_launcher_x",
        "grenade_launcher_y",
        "snd_shoot_grenade",
        "snd_reload_grenade",
        "snd_switch",
        "snd_reload_empty",
        "f_mode",
        "scope_texture",
        "new_scope_zoom",
        "scope_zoom_step_count",
        "snd_gyro",
        "snd_zoomin",
        "snd_zoomout",
        "vision_present",
        "vis_frame_speed",
        "vis_frame_color",
        "found_snd",
        "handling_factor",
        "launch_speed",
        "grenade_flame_particles",
        "snd_shoot4",
        "snd_shoot5",
        "cam_relax_speed_ai",
        "scope_exclude_bones",
        "class",
        "snd_reload_1",
        "silencer_flame_particles",
        "snd_shoot_1",
        "lens_texture",
        "lens_texture_x",
        "lens_texture_y",
        "lens_texture_w",
        "lens_texture_h",
        "ironsight_zoom_factor",
        "grenade_vel",
        "script_description",
        "npc_put_in_slot",
        "tracers",
        "can_trade",
        "sprint_allowed",
        "max_zoom_factor",
        "fragment_speed",
        "explode_duration",
        "snd_explode",
        "grenade_bone",
        "rocket_class",
        "wallmark_section",
        "cam_dispersion_frac",
        "PDM_disp_crouch",
        "PDM_disp_crouch_no_acc",
        "script_binding",
        "light_brightness",
        "light_color_animmator",
        "tracer_trail_scale",
        "tracer_start_length",
        "tracer_width",
        "custom_crosshair",
        "use_crosshair",
        "ui_show_condition",
        "attach_angle_offset",
        "attach_position_offset",
        "attach_bone_name",
        "show_ammo",
        "disp_vel_factor",
        "disp_crouch_factor",
        "disp_jump_factor",
        "vis_script_objects",
        "vis_script_valid",
        "vis_script_color",
        "af_medusa",
        "af_cristall_flower",
        "af_night_star",
        "af_vyvert",
        "af_gravi",
        "af_gold_fish",
        "af_blood",
        "af_mincer_meat",
        "zone_mincer_weak",
        "af_electra_sparkler",
        "af_electra_flash",
        "af_electra_moonlight",
        "af_drops",
        "af_fireball",
        "af_cristall",
        "af_ameba_slime",
        "af_ameba_slug",
        "af_ameba_mica",
        "zoom_hide_crosshair",
        "af_soul",
        "grenade_launcher_exclude_bones",
        "script_briefinfo",
        "default_to_ruck",
    }


class MonsterPartResource(BaseItemResource):
    _model_cls = MonsterPart

    _exclude_fields = {
        *BaseItemResource._exclude_fields,
        "monster_part",
        "belt",
    }


class OutfitResource(BaseItemResource):
    _model_cls = Outfit

    _fields = [
        *BaseItemResource._fields,
        DecimalField("burn_protection"),
        DecimalField("strike_protection"),
        DecimalField("shock_protection"),
        DecimalField("wound_protection"),
        DecimalField("radiation_protection"),
        DecimalField("telepatic_protection"),
        DecimalField("chemical_burn_protection"),
        DecimalField("explosion_protection"),
        DecimalField("fire_wound_protection"),
    ]

    _exclude_fields = {
        *BaseItemResource._exclude_fields,
        "immunities_sect",
        "actor_visual",
        "npc_visual",
        "full_icon_name",
        "bleeding_restore_speed",
        "power_loss",
        "bones_koeff_protection",
        "class",
        "additional_inventory_weight",
        "additional_inventory_weight2",
        "script_binding",
        "batteries",
        "discharge_moving",
        "discharge_sprint",
        "discharge_jump",
        "snd_cant_sprint",
        "snd_cant_jump",
        "power_restore_speed",
        "health_restore_speed",
        "satiety_restore_speed",

    }


class BaseArtefactResource(BaseItemResource):
    _model_cls = Artefact
    _exclude_fields = {
        *BaseItemResource._exclude_fields,
        "jump_height",
        "particles",
        "lights_enabled",
        "trail_light_color",
        "trail_light_range",
    }

class TrueArtefactResource(BaseArtefactResource):
    _model_cls = TrueArtefact
    _exclude_fields = {
        *BaseArtefactResource._exclude_fields,
        "allow_inertion",
        "artefact_activation_seq",
        "script_binding",
        "slot",
        "belt",
        "position",
        "attach_angle_offset",
        "attach_position_offset",
        "attach_bone_name",
        "hud",
        "can_take",
        "particles_bone",
        "default_to_ruck",
    }

    _fields = [
        *BaseArtefactResource._fields,
        DecimalField("inventory_radiation", required=False),
        DecimalField("health_restore_speed", required=False),
        DecimalField("burn_immunity", required=False),
        DecimalField("strike_immunity", required=False),
        DecimalField("shock_immunity", required=False),
        DecimalField("wound_immunity", required=False),
        DecimalField("radiation_immunity", required=False),
        DecimalField("telepatic_immunity", required=False),
        DecimalField("chemical_burn_immunity", required=False),
        DecimalField("explosion_immunity", required=False),
        DecimalField("fire_wound_immunity", required=False),
        DecimalField("power_restore_speed", required=False),
        DecimalField("additional_weight", required=False),
        DecimalField("radiation_restore_speed", required=False),
        DecimalField("bleeding_restore_speed", required=False),
        DecimalField("psy_health_restore_speed", required=False),
        DecimalField("satiety_restore_speed", required=False),
        DecimalField("jump_speed_delta", required=False),
    ]


class CapsAnomResource(BaseArtefactResource):
    _model_cls = CapsAnom
    _exclude_fields = {
        *BaseArtefactResource._exclude_fields,
        "caps_anom",
        "slot",
        "belt",
        "artefact_activation_seq",
        "hud",
        "npc_put_in_slot",
    }

class MonsterEmbrionResource(BaseArtefactResource):
    _model_cls = MonsterEmbrion
    _exclude_fields = {
        *BaseArtefactResource._exclude_fields,
        "cocoon",
        "slot",
        "belt",
        "artefact_activation_seq",
        "hud",
        "npc_put_in_slot",
    }


class OtherResource(BaseItemResource):
    _model_cls = Other

