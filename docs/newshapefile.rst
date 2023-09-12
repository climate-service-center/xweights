.. highlight:: shell
	       
==============================	       
How to add your own shape file
==============================

Hier eine Anleitung, wie du weitere Regionen hinzufügen kannst (am Beispiel SREX):
..................................................................................

Erstelle in meinen repository test_data einen neuen branch.
Füge im Verzeichnis shp deinen gezippten shape file hinzu und pushe das Ganze.
Nun kannst du einen pull request stellen.
Erstelle einen neuen branch in weights.

Editiere die Datei

.. code-block:: console  

		xweights/_regions.py:
   
L.51: Erweiter die Liste um den Namen deiner neuen Region.

.. code-block:: console

		self.regions = ["counties", "counties_merged", "states", "prudence", "srex"]

Füge am Ende der

.. code-block:: console

		__init__-Funktion self.srex=SREX()

Kopiere die Klasse Counties_merged und füge sie als neue Klasse unter dem Namen SREX hinzu:

.. code-block:: console

		class SREX:
		      def __init__(self):
		      self.description = (
		      "S-REX regions"
		      )
		      self.geodataframe = self._srex()
		      self.selection = "name"

		def _srex(self):
		    url_base = (
		    "https://github.com/ludwiglierhammer/test_data/raw/main/shp"  # noqa
		    )
		    url = os.path.join(
		          url_base, "<name_deiner_zip_datei>"
			  )
		    shape_zip = _pooch_retrieve(
                    url,
                    known_hash="2ca82af334aee2afdcce4799d5cc1ce50ce7bd0710c9ec39e6378519df60ad7a",  # noqa
                     )
                    return _get_geodataframe(shape_zip, name="SREX_Region")


Den known_hash kannst du mit dem HASH deiner gezippten Datei ersetzen. Dieser wird dir angezeigt, wenn du folgendes ausführst:

.. code-block:: console
		
		xweights which_regions

