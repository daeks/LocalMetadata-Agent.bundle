import os, json, hashlib

METADATA_FLAG = '.plexmetadata'

def Start():
  pass
  
def ValidatePrefs():
  pass
    
class LocalMetadataAgent(Agent.TV_Shows):
  name = 'Local Metadata Agent (TV)'
  languages = [Locale.Language.NoLanguage]
  primary_provider = False
  contributes_to = ['com.plexapp.agents.none', 'com.plexapp.agents.thetvdb', 'com.plexapp.agents.themoviedb']

  def search(self, results, media, lang):
    if media.primary_agent == 'com.plexapp.agents.none':
      results.Append(MetadataSearchResult(id = media.id, name = media.show, score = 100))
    else:
      results.Append(MetadataSearchResult(id = media.primary_metadata.id, score = 100))

  def update(self, metadata, media, lang):
    path = os.path.dirname(os.path.dirname(media.children[0].children[0].items[0].parts[0].file))
    Log('[METADATA] Searching for metadata in %s' % (path))
    if os.path.isfile(os.path.join(path, METADATA_FLAG)):
      try:
        Log('[METADATA] Found metadata in %s' % (path))
        data = Core.storage.load(os.path.join(path, METADATA_FLAG)).decode('utf-8', 'ignore').encode('utf-8')
        json_object = json.loads(data)
        for key, value in json_object.iteritems():
          if key == 'posters':
            for poster in json_object[key]:
              if poster not in metadata.posters:
                metadata.posters[poster] = Proxy.Media(Core.storage.load(poster), sort_order=1)
          elif key == 'art':
            for art in json_object[key]:
              if art not in metadata.art:
                metadata.art[art] = Proxy.Media(Core.storage.load(art), sort_order=1)
          elif key == 'seasons':
            for snum, season in media.seasons.iteritems():
              Log('[METADATA] Parsing season %s' % season.index)
              if ('%02d' % int(season.index)) in json_object[key]:
                season_json_object = json_object[key][('%02d' % int(season.index))]
                Log('[METADATA] Found season %s - %s' % (season.index, season_json_object))
                for skey, svalue in season_json_object.iteritems():
                  if skey == 'posters':
                    for poster in season_json_object[key]:
                      if poster not in season.posters:
                        season.posters[poster] = Proxy.Media(Core.storage.load(poster), sort_order=1)
                  elif key == 'art':
                    for art in season_json_object[key]:
                      if art not in season.art:
                        season.art[art] = Proxy.Media(Core.storage.load(art), sort_order=1)
                  elif skey == 'episodes':
                    for enum, episode in season.episodes.iteritems():
                      Log('[METADATA] Parsing season %s - episode %s' % (season.index, episode.index))
                      if ('%02d' % int(episode.index)) in season_json_object[skey]:
                        episode_json_object = season_json_object[skey][('%02d' % int(episode.index))]
                        Log('[METADATA] Found season %s - episode %s - %s' % (season.index, episode.index, episode_json_object))
                        for ekey, evalue in episode_json_object.iteritems():
                          setattribute(self, metadata.seasons[season.index].episodes[episode.index], ekey, evalue) 
                  else:
                    setattribute(self, metadata.seasons[season.index], skey, svalue)
          else:
            setattribute(self, metadata, key, value)
      except Exception as ex:
        Log('[METADATA] Could not load data from metadata: %s' % (ex))

def setattribute(self, metadata, key, value):
  try:
    if hasattr(metadata, 'attrs'):
      if not metadata.attrs.get(key) is None:
        attr = metadata.attrs.get(key)
        if isinstance(attr, Framework.modelling.attributes.StringObject):
          setattr(metadata, key, value)
        elif isinstance(attr, Framework.modelling.attributes.IntegerObject):
          setattr(metadata, key, int(value))
        elif isinstance(attr, Framework.modelling.attributes.FloatObject):
          setattr(metadata, key, float(value))
        elif isinstance(attr, Framework.modelling.attributes.DateObject):
          setattr(metadata, key, Datetime.ParseDate(value).date())
        else:
          setattr(metadata, key, value)
    else:
      setattr(metadata, key, value)
  except Exception as ex:
    Log('[METADATA] Could not store data to metadata: %s / %s - %s' % (key, value, ex))

def dump(self, obj):
  for attr in dir(obj):
    Log('[METADATA] obj.%s = %s' % (attr, getattr(obj, attr)))
  Log('[METADATA] obj has been dumped')