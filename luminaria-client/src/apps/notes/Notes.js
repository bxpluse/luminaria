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
import Container from "react-bootstrap/Container";
import MyButton from "../../components/MyButton";
import Request from "../../Requests";
import './Notes.css';

const toolbarPlugin = createToolbarPlugin();
const { Toolbar } = toolbarPlugin;
const plugins = [toolbarPlugin];

function Notes() {

    return (
        <Container>
            <CustomEditor />
        </Container>
    )
}

function CustomEditor() {

    const [saveDisabled, setSaveDisabled] = useState(true);
    const [previousContent, setPreviousContent] = useState(null);
    const [editorState, setEditorState] = useState(createEditorStateWithText(''));
    const editor = React.useRef(null);

    useEffect(() => {
        Request.POST_JSON('/exec/notes/load', {}).then(data => {
            const contentState = convertFromRaw(JSON.parse(data['content']));
            const editorStateTemp = EditorState.createWithContent(contentState);
            setEditorState(editorStateTemp);
            setPreviousContent(stateToString(editorStateTemp));
        });
    }, []);

    function onChange(editorState){
        setEditorState(editorState);
        if (previousContent !== null) {
            setSaveDisabled(previousContent === stateToString(editorState));
        }
    }

    async function save(content) {
        const body = {content: content};
        await Request.POST_JSON('/exec/notes/save', body);
        setSaveDisabled(true);
        setPreviousContent(stateToString(editorState));
    }

    function focusEditor() {
        editor.current.focus();
    }

    return (
        <div>
            <h2>Notebook</h2>
            <br/>
            <div className={"editor"}
                 onClick={focusEditor}>
                <div style={{ padding:"1em" }}>
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
                    />
                </div>
            </div>
            <MyButton text={"Save"}
                      disabled={saveDisabled}
                      onClick={() => save(stateToString(editorState))}
            />
        </div>
    );
}

function stateToString(state) {
    return JSON.stringify(convertToRaw(state.getCurrentContent()))
}


export default Notes;