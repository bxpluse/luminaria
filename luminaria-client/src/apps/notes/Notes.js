import {
    BoldButton,
    ItalicButton,
    OrderedListButton,
    UnderlineButton,
    UnorderedListButton
} from '@draft-js-plugins/buttons';
import Editor, {createEditorStateWithText} from '@draft-js-plugins/editor';
import createToolbarPlugin, {Separator,} from '@draft-js-plugins/static-toolbar';
import '@draft-js-plugins/static-toolbar/lib/plugin.css';
import {convertFromRaw, convertToRaw, EditorState} from 'draft-js';
import React, {useEffect, useState} from 'react';
import {Tooltip} from 'react-bootstrap';
import Container from 'react-bootstrap/Container';
import InfoSymbol from '../../components/InfoSymbol';
import MyButton from '../../components/MyButton';
import Request from '../../Requests';
import DateUtil from '../../util/DateUtil';
import './Notes.css';

const toolbarPlugin = createToolbarPlugin();
const {Toolbar} = toolbarPlugin;
const plugins = [toolbarPlugin];

function Notes() {

    return (
        <Container>
            <CustomEditor/>
        </Container>
    )
}

function CustomEditor() {

    const [saveDisabled, setSaveDisabled] = useState(true);
    const [previousContent, setPreviousContent] = useState(null);
    const [editorState, setEditorState] = useState(createEditorStateWithText(''));
    const [currentOffset, setCurrentOffset] = useState(0);
    const [dateTimeCreated, setDateTimeCreated] = useState('');
    const [maxOffset, setMaxOffset] = useState(2);
    const editor = React.useRef(null);

    useEffect(() => {
        fetch_note(0);
    }, []);

    function fetch_note(offset) {
        Request.POST_JSON('/exec/notes/load', {'offset': offset}).then(data => {
            const note = data['note'];
            const contentState = convertFromRaw(JSON.parse(note['content']));
            const editorStateTemp = EditorState.createWithContent(contentState);
            setEditorState(editorStateTemp);
            setCurrentOffset(offset);
            setDateTimeCreated(DateUtil.parse(note['datetime_created']));
            if (offset === 0) {
                setMaxOffset(note['max_offset']);
                setPreviousContent(stateToString(editorStateTemp));
            }
        });
    }

    function onChange(editorState) {
        setEditorState(editorState);
        if (previousContent !== null) {
            setSaveDisabled(previousContent === stateToString(editorState));
        }
    }

    const renderTooltip = () => (
        <Tooltip id={'tooltip'} className='mytooltip'>
            <p>{dateTimeCreated}</p>
        </Tooltip>
    );

    async function save(content) {
        const body = {content: content};
        await Request.POST_JSON('/exec/notes/save', body);
        setSaveDisabled(true);
        setPreviousContent(stateToString(editorState));
        fetch_note(0);
    }

    function focusEditor() {
        editor.current.focus();
    }

    let historyClass = 'unselectable text-muted';
    if (currentOffset >= maxOffset - 1) {
        historyClass += ' history-exhausted-span';
    }

    return (
        <div>
            <h2>Notebook</h2>

            <div>
                {currentOffset < maxOffset - 1 ?
                    <MyButton text='<' variant='link' onClick={() => fetch_note(currentOffset + 1)}/>
                    : null
                }
                <span className={historyClass}>&nbsp;History <InfoSymbol onHover={renderTooltip()}/>&nbsp;</span>
                {currentOffset !== 0 ?
                    <MyButton text='>' variant='link' onClick={() => fetch_note(currentOffset - 1)}/>
                    : null
                }
            </div>

            <div className={'editor'}
                 onClick={focusEditor}>
                <div style={{padding: '1em'}}>
                    <Toolbar>
                        {
                            (externalProps) => (
                                <div>
                                    <BoldButton {...externalProps} />
                                    <ItalicButton {...externalProps} />
                                    <UnderlineButton {...externalProps} />
                                    <Separator {...externalProps} />
                                    <UnorderedListButton {...externalProps} />
                                    <OrderedListButton {...externalProps} />
                                </div>
                            )
                        }
                    </Toolbar>
                    <br/>
                    <Editor
                        editorState={editorState}
                        onChange={onChange}
                        plugins={plugins}
                        ref={editor}
                        readOnly={currentOffset !== 0}
                    />
                </div>
            </div>
            {currentOffset === 0 ?
                <MyButton text={'Save'}
                          disabled={saveDisabled}
                          onClick={() => save(stateToString(editorState))}
                /> : null
            }
        </div>
    );
}

function stateToString(state) {
    return JSON.stringify(convertToRaw(state.getCurrentContent()))
}


export default Notes;