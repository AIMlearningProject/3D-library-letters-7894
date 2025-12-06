"""
Translation system for NamePlate Studio Pro
Supports English and Finnish
"""

class Translator:
    """Handles UI translations"""

    def __init__(self):
        self.current_language = 'en'
        self.translations = {
            'en': self._get_english_translations(),
            'fi': self._get_finnish_translations()
        }

    def set_language(self, lang_code):
        """Set current language"""
        if lang_code in self.translations:
            self.current_language = lang_code
            return True
        return False

    def get(self, key, default=None):
        """Get translation for key"""
        trans = self.translations.get(self.current_language, {})
        return trans.get(key, default or key)

    def _get_english_translations(self):
        """English translations"""
        return {
            # Application
            'app_name': 'NamePlate Studio Pro',
            'ready': 'Ready',
            'design_updated': 'Design updated',

            # File Menu
            'file': '&File',
            'new_project': '&New Project',
            'open_project': '&Open Project...',
            'save_project': '&Save Project',
            'save_project_as': 'Save Project &As...',
            'recent_projects': 'Recent Projects',
            'export_to_stl': '&Export to STL...',
            'export_to_blend': 'Export to Blend...',
            'exit': 'E&xit',

            # Edit Menu
            'edit': '&Edit',
            'undo': '&Undo',
            'redo': '&Redo',
            'preferences': '&Preferences...',

            # View Menu
            'view': '&View',
            'zoom_in': 'Zoom &In',
            'zoom_out': 'Zoom &Out',
            'fit_to_view': '&Fit to View',
            'reset_view': '&Reset View',
            'language': 'Language',
            'english': 'English',
            'finnish': 'Suomi (Finnish)',

            # Tools Menu
            'tools': '&Tools',
            'validate_design': '&Validate Design',
            'batch_processing': '&Batch Processing...',
            'add_qr_code': 'Add &QR Code...',
            'add_logo': 'Add &Logo/Image...',

            # Help Menu
            'help': '&Help',
            'documentation': '&Documentation',
            'about': '&About',

            # Design Panel
            'text_content': 'Text Content',
            'line_1': 'Line 1:',
            'line_2': 'Line 2:',
            'dimensions': 'Dimensions (mm)',
            'plate_length': 'Plate Length:',
            'plate_width': 'Plate Width:',
            'plate_thickness': 'Plate Thickness:',
            'letter_depth': 'Letter Depth:',
            'typography': 'Typography',
            'font': 'Font:',
            'text_size': 'Text Size:',
            'line_spacing': 'Line Spacing:',
            'material_finish': 'Material & Finish',
            'material': 'Material:',
            'finish': 'Finish:',
            'reset_to_default': 'Reset to Default',
            'generate_preview': 'Generate Preview',

            # Template Panel
            'templates': 'Templates',
            'library_sign': 'Library Sign',
            'door_plate': 'Door Plate',
            'desk_nameplate': 'Desk Nameplate',
            'wall_sign': 'Wall Sign',
            'custom': 'Custom',

            # Preview Panel
            'view_mode': 'View Mode',
            'view_3d': '3D',
            'view_top': 'Top',
            'view_front': 'Front',
            'view_side': 'Side',
            'zoom': 'Zoom:',
            'no_design_loaded': 'No design loaded',
            'preview_placeholder': 'Preview will appear here\n\nModify design settings to see changes',

            # Materials
            'pla_standard': 'PLA Standard',
            'petg_glossy': 'PETG Glossy',
            'abs': 'ABS',
            'wood_fill': 'Wood Fill',
            'carbon_fiber': 'Carbon Fiber',

            # Finishes
            'smooth': 'Smooth (post-processed)',
            'standard': 'Standard (as-printed)',
            'textured': 'Textured',

            # Messages
            'template_loaded': 'Template loaded',
            'project_saved': 'Project saved successfully!',
            'error': 'Error',
            'success': 'Success',
            'warning': 'Warning',
            'info': 'Information',

            # Dialogs
            'new_project_confirm': 'Create a new project? Unsaved changes will be lost.',
            'feature_coming_soon': 'Feature Coming Soon',
            'stl_export_message': 'STL export is not yet implemented.\nThis feature will be available in a future update.',
            'blend_export_message': 'Blender export is not yet implemented.\nThis feature will be available in a future update.',
            'language_changed_message': 'Language changed! Please restart the application for all changes to take effect.',
        }

    def _get_finnish_translations(self):
        """Finnish translations"""
        return {
            # Application
            'app_name': 'NamePlate Studio Pro',
            'ready': 'Valmis',
            'design_updated': 'Malli päivitetty',

            # File Menu
            'file': '&Tiedosto',
            'new_project': '&Uusi projekti',
            'open_project': '&Avaa projekti...',
            'save_project': '&Tallenna projekti',
            'save_project_as': 'Tallenna projekti &nimellä...',
            'recent_projects': 'Viimeisimmät projektit',
            'export_to_stl': '&Vie STL-muotoon...',
            'export_to_blend': 'Vie Blend-muotoon...',
            'exit': '&Poistu',

            # Edit Menu
            'edit': '&Muokkaa',
            'undo': '&Kumoa',
            'redo': '&Tee uudelleen',
            'preferences': '&Asetukset...',

            # View Menu
            'view': '&Näytä',
            'zoom_in': 'Lähennä',
            'zoom_out': 'Loitonna',
            'fit_to_view': 'Sovita näkymään',
            'reset_view': 'Palauta näkymä',
            'language': 'Kieli',
            'english': 'English (Englanti)',
            'finnish': 'Suomi',

            # Tools Menu
            'tools': '&Työkalut',
            'validate_design': '&Tarkista malli',
            'batch_processing': '&Eräkäsittely...',
            'add_qr_code': 'Lisää &QR-koodi...',
            'add_logo': 'Lisää &logo/kuva...',

            # Help Menu
            'help': '&Ohje',
            'documentation': '&Dokumentaatio',
            'about': '&Tietoja',

            # Design Panel
            'text_content': 'Tekstin sisältö',
            'line_1': 'Rivi 1:',
            'line_2': 'Rivi 2:',
            'dimensions': 'Mitat (mm)',
            'plate_length': 'Levyn pituus:',
            'plate_width': 'Levyn leveys:',
            'plate_thickness': 'Levyn paksuus:',
            'letter_depth': 'Kirjainten syvyys:',
            'typography': 'Typografia',
            'font': 'Fontti:',
            'text_size': 'Tekstin koko:',
            'line_spacing': 'Riviväli:',
            'material_finish': 'Materiaali ja viimeistely',
            'material': 'Materiaali:',
            'finish': 'Viimeistely:',
            'reset_to_default': 'Palauta oletukset',
            'generate_preview': 'Luo esikatselu',

            # Template Panel
            'templates': 'Mallipohjat',
            'library_sign': 'Kirjaston kyltti',
            'door_plate': 'Ovikilpi',
            'desk_nameplate': 'Pöytäkyltti',
            'wall_sign': 'Seinäkyltti',
            'custom': 'Mukautettu',

            # Preview Panel
            'view_mode': 'Näkymätila',
            'view_3d': '3D',
            'view_top': 'Yläpuoli',
            'view_front': 'Etupuoli',
            'view_side': 'Sivusta',
            'zoom': 'Zoomaus:',
            'no_design_loaded': 'Ei mallia ladattuna',
            'preview_placeholder': 'Esikatselu näkyy tässä\n\nMuokkaa asetuksia nähdäksesi muutokset',

            # Materials
            'pla_standard': 'PLA Standardi',
            'petg_glossy': 'PETG Kiiltävä',
            'abs': 'ABS',
            'wood_fill': 'Puutäyte',
            'carbon_fiber': 'Hiilikuitu',

            # Finishes
            'smooth': 'Sileä (jälkikäsitelty)',
            'standard': 'Standardi (tulostettu)',
            'textured': 'Kuvioitu',

            # Messages
            'template_loaded': 'Mallipohja ladattu',
            'project_saved': 'Projekti tallennettu onnistuneesti!',
            'error': 'Virhe',
            'success': 'Onnistui',
            'warning': 'Varoitus',
            'info': 'Tiedoksi',

            # Dialogs
            'new_project_confirm': 'Luodaanko uusi projekti? Tallentamattomat muutokset menetetään.',
            'feature_coming_soon': 'Ominaisuus tulossa pian',
            'stl_export_message': 'STL-vienti ei ole vielä toteutettu.\nTämä ominaisuus tulee saataville tulevassa päivityksessä.',
            'blend_export_message': 'Blend-vienti ei ole vielä toteutettu.\nTämä ominaisuus tulee saataville tulevassa päivityksessä.',
            'language_changed_message': 'Kieli vaihdettu! Käynnistä sovellus uudelleen, jotta kaikki muutokset tulevat voimaan.',
        }

# Global translator instance
_translator = Translator()

def get_translator():
    """Get global translator instance"""
    return _translator

def tr(key, default=None):
    """Quick translation function"""
    return _translator.get(key, default)
