# Pebble Community Events

This repository aims at providing an easy way for the Pebble community to inform each other of various events happening around them. We encourage each and every event organizer to create a Pull Request with the details of their own event. The format and function of the files is provided below:

## events.yml

This file stores all the information about various Pebble events happening all around the world. They can happen physically or online! There are a couple categories to choose from. Share your passion!

An example excerpt from the list looks as follows:
```yaml
- title: Pyrkon Pebble meetup
  description: |
    A short meeting of Pebble enthustiasts at Pyrkon!
    Hope to see you there!
  website: https://website.for/your-event
  type: Choose one of: Meetup
  start_date: 2056-07-08
  end_date: 2056-07-09
  all_day: true
  location: Poznań
  latitude: 40.741895
  longitude: -73.989308
```

## locations.yml

This file stores all the information about various clubs, groups and local communities that organize events and meetings about Pebbles. The information provided here differs from what is in the Events file, and is meant to provide information to the community members about the community existing, its location, and information on how to find out more about it.

An example excerpt from the list looks as follows:

```yaml
- title: Big Pebble
  description: |
    We organize monthly meetings with the community in Central Park!
    We would love to see you there. Take your dogs on a walk or take part in a communal run.
  website: https://exampleeventswebsite.com/bigpebble
  location: Central Park
  latitude: 40.741895
  longitude: -73.989308
```
