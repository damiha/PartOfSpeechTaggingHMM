import React, { useState } from 'react';
import './App.css';

const App = () => {

  const [inputText, setInputText] = useState('');
  const [taggedWords, setTaggedWords] = useState([]);

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  const handleSubmit = (taggingType) => {
    fetch('http://127.0.0.1:5000/tag', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: inputText,
        tagger: taggingType,
      }),
    })
    .then(response => response.json())
    .then(data => {
      console.log(data.tagged);
      setTaggedWords(data.tagged);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  };

  const tags = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB', '$', '#', '``', "''", '(', ')', ',', '.', ':', '-LRB-', '-RRB-', '-NONE-'];

  const getTagDescription = (tag) => {
    const tagDescriptions = {
      'CC': 'Coordinating conjunction',
      'CD': 'Cardinal number',
      'DT': 'Determiner',
      'EX': 'Existential there',
      'FW': 'Foreign word',
      'IN': 'Preposition or subordinating conjunction',
      'JJ': 'Adjective',
      'JJR': 'Adjective, comparative',
      'JJS': 'Adjective, superlative',
      'LS': 'List item marker',
      'MD': 'Modal',
      'NN': 'Noun, singular or mass',
      'NNS': 'Noun, plural',
      'NNP': 'Proper noun, singular',
      'NNPS': 'Proper noun, plural',
      'PDT': 'Predeterminer',
      'POS': 'Possessive ending',
      'PRP': 'Personal pronoun',
      'PRP$': 'Possessive pronoun',
      'RB': 'Adverb',
      'RBR': 'Adverb, comparative',
      'RBS': 'Adverb, superlative',
      'RP': 'Particle',
      'SYM': 'Symbol',
      'TO': 'to',
      'UH': 'Interjection',
      'VB': 'Verb, base form',
      'VBD': 'Verb, past tense',
      'VBG': 'Verb, gerund or present participle',
      'VBN': 'Verb, past participle',
      'VBP': 'Verb, non-3rd person singular present',
      'VBZ': 'Verb, 3rd person singular present',
      'WDT': 'Wh-determiner',
      'WP': 'Wh-pronoun',
      'WP$': 'Possessive wh-pronoun',
      'WRB': 'Wh-adverb',
      '$': 'Dollar sign',
      '#': 'Number sign',
      '``': 'Opening quotation mark',
      "''": 'Closing quotation mark',
      '(': 'Left parenthesis',
      ')': 'Right parenthesis',
      ',': 'Comma',
      '.': 'Sentence-final punctuation',
      ':': 'Colon or ellipsis',
      '-LRB-': 'Left bracket',
      '-RRB-': 'Right bracket',
      '-NONE-': 'No tag',
    };
  
    return tagDescriptions[tag] || tag;
  };
  
  const getTagColor = (tag) => {
    const tagColors = {
      'CC': '#D6EAF8',
      'CD': '#D4EFDF',
      'DT': '#FADBD8',
      'EX': '#FDEBD0',
      'FW': '#EBDEF0',
      'IN': '#D5DBDB',
      'JJ': '#D6DBDF',
      'JJR': '#A9DFBF',
      'JJS': '#AED6F1',
      'LS': '#F9E79F',
      'MD': '#ABEBC6',
      'NN': '#A3D1F0',
      'NNS': '#A9CCE3',
      'NNP': '#A2D9CE',
      'NNPS': '#A9CCE3',
      'PDT': '#D7BDE2',
      'POS': '#D2B4DE',
      'PRP': '#AED6F1',
      'PRP$': '#F5B7B1',
      'RB': '#D7DBDD',
      'RBR': '#FAD7A0',
      'RBS': '#F5CBA7',
      'RP': '#F7DC6F',
      'SYM': '#E59866',
      'TO': '#F0B27A',
      'UH': '#CD6155',
      'VB': '#AEB6BF',
      'VBD': '#A9DFBF',
      'VBG': '#A3E4D7',
      'VBN': '#A2D9CE',
      'VBP': '#AED6F1',
      'VBZ': '#A9CCE3',
      'WDT': '#F5B7B1',
      'WP': '#F5CBA7',
      'WP$': '#F9E79F',
      'WRB': '#F4D03F',
      '$': '#B2BABB',
      '#': '#AEB6BF',
      '``': '#D2B4DE',
      "''": '#D7BDE2',
      '(': '#EAF2F8',
      ')': '#EAF2F8'}

      return tagColors[tag] || tag;
    };

  const renderTaggedText = () => {
    return taggedWords.map((sentence, sIndex) => (
      <div key={sIndex} className="sentence">
        {sentence.map(([word, tag], wIndex) => (
          <div key={wIndex} className="tagged-word">
            <span style={{ backgroundColor: getTagColor(tag) }}>
              {word}
            </span>
            <span className="tag-description">
              {getTagDescription(tag)}
            </span>
          </div>
        ))}
      </div>
    ));
  };
  

  const categories = tags.map(tag => ({
    name: getTagDescription(tag),
    color: getTagColor(tag),
  }));

  return (
    <div className="App">
      <h1>POS-Tagging</h1>
      <textarea 
        value={inputText} 
        onChange={handleInputChange}
        className="text-input"
      />
      <div className="buttons">
        <button onClick={() => handleSubmit('naive')}>Tag naively</button>
        <button onClick={() => handleSubmit('hmm')}>Tag with HMM</button>
      </div>
      <div className="tagged-text">
        {renderTaggedText()}
      </div>
      <div className="categories-box">
        {categories.map((category, index) => (
          <div key={index} className="category-item">
            <span style={{ backgroundColor: category.color }} className="color-circle"></span>
            {category.name}
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;


