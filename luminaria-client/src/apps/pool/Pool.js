import React, {useEffect, useState} from "react";
import {Col} from 'react-bootstrap';
import Accordion from 'react-bootstrap/Accordion'
import Badge from 'react-bootstrap/Badge'
import Collapse from 'react-bootstrap/Collapse'
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form'
import InputGroup from 'react-bootstrap/InputGroup'
import Jumbotron from "react-bootstrap/Jumbotron";
import Tab from 'react-bootstrap/Tab'
import Table from 'react-bootstrap/Table'
import Tabs from 'react-bootstrap/Tabs'
import MyButton from "../../components/MyButton";
import MyModal from "../../components/MyModal";
import Request from "../../Requests";
import DateUtil from "../../util/DateUtil";
import MathUtil from '../../util/MathUtil'
import './Pool.css';

function Pool() {

    const [pools, setPools] = useState([]);
    const [entries, setEntries] = useState({});
    const DASHBOARD = "Dashboard";

    useEffect(() => {
        Request.POST_JSON('/exec/pool/fetchAllPoolNames', {}).then(res => {
            setPools(res['pools']);
        });
    }, []);

    async function handleSelect(poolName) {
        if(poolName !== DASHBOARD){
            const body = {poolName: poolName};
            await Request.POST_JSON('/exec/pool/fetchPoolEntriesByName', body).then(data => {
                setEntries((prevDivState) => {
                    return { ...prevDivState, [poolName]: data.entries };
                });
            });
        }
    }

    let poolTabs = [];
    for(let i = 0; i < pools.length; i++){
        const poolItem = pools[i];
        poolTabs.push(
            <Tab key={poolItem['pool_name']} eventKey={poolItem['pool_name']} title={poolItem['pool_name']}>
                <SinglePool pool={poolItem} entries={entries[poolItem['pool_name']]}
                            rerender={(value) => handleSelect(value)}/>
            </Tab>
        );
    }

    return (
        <Container>
            <Tabs onSelect={(k) => handleSelect(k)}>
                <Tab eventKey={DASHBOARD} title={DASHBOARD}>
                    <CreatePool/>
                </Tab>
                {poolTabs}
            </Tabs>
        </Container>
    );
}

function SinglePool(props) {
    const setTrade = new Set(['BUY', 'SELL']);
    const [show, setShow] = useState(false);
    const [body, setBody] = useState('');
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const pool = props.pool;
    const entries = props.entries;

    const stockRowNum = 5;
    const optionRowNum = 7;
    const transactionRowNum = 3;
    const totalSpan = stockRowNum * optionRowNum * transactionRowNum;

    let history = [];

    if (entries !== undefined){
        for(let i = 0; i < entries.length; i++){
            let divider = stockRowNum;
            const entry = entries[i];
            const multiplier = entry['instrument'] === 'OPTION'? 100 : 1;
            if (entry['instrument'] !== 'STOCK') {
                divider = optionRowNum
            }

            if (setTrade.has(entry['action'])) {
                const colSpan = totalSpan / divider;
                history.push(
                    <tr key={i}>
                        <td colSpan={colSpan} className='align-center'>
                            {entry['action']}&nbsp;
                            {entry['note'] !== ''?
                                <Badge onClick={() => {handleShow(); setBody(entry['note'])}}
                                       variant="info">Note
                                </Badge>: undefined
                            }
                        </td>
                        <td colSpan={colSpan} className='align-right'> {entry['amount']}</td>
                        <td colSpan={colSpan} className='align-center'>{entry['symbol']}</td>
                        <td colSpan={colSpan} className='align-right'>
                            ${entry['price'].toFixed(2)}   |
                            ${(entry['amount'] * entry['price'] * multiplier).toFixed(2)}
                        </td>
                        <td colSpan={colSpan} className='align-center'>{entry['date'] + ' ' + entry['time']}</td>
                        {entry['strike'] !== null?
                            <td colSpan={colSpan} className='align-center'>Spot: {entry['spot']}
                                Strike: {entry['strike']} </td>: undefined}
                        {entry['expiry_date'] !== null? <td
                            colSpan={colSpan} className='align-center'>{entry['expiry_date']}</td>: undefined}
                    </tr>
                );
            } else {
                const colSpan = totalSpan / transactionRowNum;
                history.push(
                    <tr key={i}>
                        <td colSpan={colSpan} className='align-center'>{entry['action']}</td>
                        <td colSpan={colSpan} className='align-right'>${entry['amount']}</td>
                        <td colSpan={colSpan} className='align-right'>{entry['date'] + ' ' + entry['time']}</td>
                    </tr>
                );
            }
        }
    }

    return (
        <div>
            <MyModal show={show} onHide={handleClose} title='Note' body={body}/>
            <SinglePoolSummary pool={pool} entries={entries}/>
            <CreateEntry poolName={pool['pool_name']} rerender={(value) => props.rerender(value)}/>
            <Table striped bordered hover>
                <thead>
                <tr>
                    <th colSpan={totalSpan} className='align-center'><h4>History</h4></th>
                </tr>
                </thead>
                <tbody>
                {history}
                </tbody>
            </Table>
        </div>
    );
}

function SinglePoolSummary(props) {

    const [netLiquidationVal, setNetLiquidationVal] = useState(0);
    const [openPositionsVal, setOpenPositionsVal] = useState(0);
    const [availableCash, setAvailableCash] = useState(0);
    const [profit, setProfit] = useState(0);

    const pool = props.pool;
    const entries = props.entries;

    useEffect(() => {
        let availableCashTemp = 0;
        let netLiquidationValTemp = 0;
        let commissionTemp = 0;
        let realizedGainsTemp = 0;
        let unrealizedGainsTemp = 0;

        let openStockPositions = {};
        // let openOptionPositions = {};

        if (entries !== undefined) {
            for (let i = 0; i < entries.length; i++) {
                const entry = entries[i];
                if (entry.action === 'DEPOSIT') {
                    availableCashTemp += entry.amount;
                } else {
                    const symbol = entry.symbol;
                    const amount = entry.amount;
                    const price = entry.price;
                    const multiplier = entry.instrument === 'OPTION'? 100 : 1;
                    const cost = amount * price * multiplier;

                    if (entry.action === 'BUY') {
                        availableCashTemp -= cost;
                        if (!(symbol in openStockPositions)) {
                            openStockPositions[symbol] = new OpenPosition(symbol, 0, price);
                        }
                        const openPosition = openStockPositions[symbol];
                        openPosition.costBasis = ((openPosition.amount * openPosition.costBasis) + (amount * price))
                            / (openPosition.amount + amount)
                        openPosition.amount += amount;

                    } else if (entry.action === 'SELL') {
                        availableCashTemp += cost;
                        if (!(symbol in openStockPositions)) {
                            openStockPositions[symbol] = new OpenPosition(symbol, 0, price);
                        }
                        const openPosition = openStockPositions[symbol];
                        realizedGainsTemp += (amount * price) - (amount * openPosition.costBasis)
                        openPosition.amount -= amount;
                    }
                    //commissionTemp += 1;
                }
            }
        }
        for (const [, position] of Object.entries(openStockPositions)) {
            unrealizedGainsTemp += position.amount * position.costBasis
        }
        availableCashTemp -= commissionTemp;
        netLiquidationValTemp += availableCashTemp + unrealizedGainsTemp;

        setNetLiquidationVal(netLiquidationValTemp);
        setAvailableCash(availableCashTemp);
        setOpenPositionsVal(unrealizedGainsTemp)
        setProfit(realizedGainsTemp)
    }, [entries, setNetLiquidationVal]);


    return(
        <Jumbotron>
            <h4>Summary</h4>
            <div>
                <Form>
                    <Form.Row>
                        <FormGroup label='Pool Name'     value={pool['pool_name']} disabled/>
                        <FormGroup label='Created on'    value={pool['datetime_created']} disabled/>
                    </Form.Row>
                    <Form.Row>
                        <FormGroup label='Est. Net Liq.' value={netLiquidationVal.toFixed(2).toString()}
                                   prepend='$' disabled/>
                        <FormGroup label='Open Pos. Val' value={openPositionsVal.toFixed(2).toString()}
                                   prepend='$' disabled/>
                        <FormGroup label='Avl. Cash'     value={availableCash.toFixed(2).toString()}
                                   prepend='$' disabled/>
                        <FormGroup label='Rlz. Profit'   value={profit.toFixed(2).toString()}
                                   prepend='$' disabled/>
                    </Form.Row>
                    <FormGroup row label='Description' as="textarea" rows={3} value={pool['description']} disabled/>
                </Form>
            </div>
        </Jumbotron>
    )
}

function CreateEntry(props) {

    const [openCreateEntryForm, setOpenCreateEntryForm] = useState(false);
    const [entryType, setEntryType] = useState('stock');
    const [saveDisabled, setSaveDisabled] = useState(true)

    const [action, setAction]           = useState('');
    const [amount, setAmount]           = useState('');
    const [symbol, setSymbol]           = useState('');
    const [price, setPrice]             = useState('');
    const [date, setDate]               = useState('');
    const [time, setTime]               = useState('');
    const [spot, setSpot]               = useState('');
    const [strike, setStrike]           = useState('');
    const [expiryDate, setExpiryDate]   = useState('');
    const [note, setNote]               = useState('');
    const [parserText, setParserText]   = useState('');

    async function saveEntry(action, amount, symbol, price, date, time, spot, strike, expiryDate, note) {
        const body = {poolName: props.poolName, instrument: entryType, entryType: entryType,
            action: action, amount: amount, symbol: symbol, price: price, date: date, time: time,
            spot: spot, strike: strike, expiryDate: expiryDate, note: note};
        await Request.POST_JSON('/exec/pool/saveEntryByName', body).then(() => {
            props.rerender(props.poolName);
        });
    }

    function reset(){
        setAmount('');
        setSymbol('');
        setPrice('');
        setDate('');
        setTime('');
        setSpot('');
        setStrike('');
        setExpiryDate('');
        setNote('');
        setParserText('');
    }

    useEffect(() => {
        if (entryType !== "option") {
            setSpot('');
            setStrike('');
            setExpiryDate('');
        }
        if (action !== "...") {
            if (action && amount && symbol && price && date && time) {
                if (entryType === "option") {
                    if (spot && strike && expiryDate) {
                        setSaveDisabled(false);
                        return;
                    }
                } else if (entryType === "stock") {
                    setSaveDisabled(false);
                    return;
                }
            }
        }
        setSaveDisabled(true);

    }, [entryType, action, amount, symbol, price, date, time, spot, strike, expiryDate]);

    function parser(string) {
        setParserText(string);
        const arr = string.trim().split('\t')

        if (arr[0] !== 'BOT' && arr[0] !== 'SLD') {
            return
        }
        if (!MathUtil.isPositiveInt(arr[1])) {
            return
        }
        if (!MathUtil.isPositiveInt(arr[3])) {
            return
        }

        const thirdArr = arr[2].split(',');
        const datetime = arr[5].split(' ');
        const date = datetime[4];
        const time = datetime[0];

        setAction(arr[0] === 'BOT' ? 'BUY' : 'SELL');
        setAmount(arr[1]);
        setSymbol(thirdArr[0]);
        setPrice(arr[3]);

        if (date === undefined) {
            setDate(DateUtil.getCurrentDate);
        } else {
            const dateFormatted = date.substring(0, 4).concat('-')
                .concat(date.substring(4, 6)).concat('-')
                .concat(date.substring(6, 8));
            setDate(dateFormatted);
        }
        setTime(time);
    }

    return (
        <div>
            <MyButton text="Create New Entry" onClick={() => setOpenCreateEntryForm(!openCreateEntryForm)}/>
            <Collapse in={openCreateEntryForm}>
                <div>
                    <Jumbotron>
                        <Form>
                            {['radio'].map((type) => (
                                <div key={`inline-${type}`} className='mb-3'>
                                    <Form.Check inline label='Stock' name='group1' type={type}
                                                onChange={() => setEntryType('stock')}
                                                checked={entryType === 'stock'}/>
                                    <Form.Check inline label='Option' name='group1' type={type}
                                                onChange={() => setEntryType('option')}
                                                checked={entryType === 'option'}
                                    />
                                    <Form.Check inline label='Transaction' name="'group1" type={type} disabled
                                                onChange={() => setEntryType('transaction')}
                                                checked={entryType === 'transaction'}/>
                                </div>
                            ))}
                            <Form.Row>
                                <Form.Group as={Col}>
                                    <Form.Label>Action</Form.Label>
                                    <Form.Control value={action} as='select' defaultValue='...'
                                                  onChange={e => setAction(e.target.value)}
                                    >
                                        <option>...</option>
                                        <option>BUY</option>
                                        <option>SELL</option>
                                    </Form.Control>
                                </Form.Group>
                                <FormGroup label='Amount' value={amount} func={setAmount}/>
                                <FormGroup label='Symbol' value={symbol} func={setSymbol} prepend={''}/>
                                <FormGroup label='Price'  value={price}  func={setPrice}  prepend={'$'}/>
                                <FormGroup label='Date'   value={date}   func={setDate}   type={'date'}/>
                                <FormGroup label='Time'   value={time}   func={setTime}   type={'time'}/>
                                { entryType === 'option' ?
                                    <>
                                        <FormGroup label='Spot'   value={spot}       func={setSpot}/>
                                        <FormGroup label='Strike' value={strike}     func={setStrike}/>
                                        <FormGroup label='Expiry' value={expiryDate} func={setExpiryDate} type='date'/>
                                    </>: null
                                }
                            </Form.Row>
                            <Accordion>
                                <Accordion.Toggle as={NoteLinkButton} eventKey='0'>
                                    > Note
                                </Accordion.Toggle>
                                <Accordion.Collapse eventKey='0'>
                                    <FormGroup row label='Note' value={note} func={setNote}/>
                                </Accordion.Collapse>
                            </Accordion>
                            <FormGroup row placeholder='Auto Parser' value={parserText} func={parser}/>
                        </Form>
                        <br/>
                        <MyButton text="Save"
                                  disabled={saveDisabled}
                                  onClick={() => {
                            saveEntry(action, amount, symbol, price, date, time, spot, strike, expiryDate, note)
                                .then(() => reset())
                        }}
                        />
                    </Jumbotron>
                </div>
            </Collapse>
            <br/><br/>
        </div>
    );
}


function CreatePool() {
    const [open, setOpen] = useState(false);
    const [createPoolName, setCreatePoolName] = useState('');
    const [createPoolDescription, setCreatePoolDescription] = useState('');
    const [createPoolInitialFund, setCreatePoolInitialFund] = useState('0');
    return (
        <div>
            <br/>
            <MyButton text='Create New Pool' onClick={() => setOpen(!open)}>click</MyButton>
            <Collapse in={open}>
                <div>
                    <Jumbotron>
                        <h4>Create a new pool</h4>
                        <Form>
                            <FormGroup label='Pool Name' value={createPoolName} func={setCreatePoolName} type='text'/>
                            <FormGroup label='Initial Fund' value={createPoolInitialFund} prepend='$'
                                       func={setCreatePoolInitialFund} type='number'
                            />
                            <FormGroup label='Description' value={createPoolDescription}
                                       func={setCreatePoolDescription} as='textarea' rows={3}/>
                        </Form>
                        <MyButton text='Save'  onClick={() =>
                            savePool(createPoolName, createPoolDescription, createPoolInitialFund)}/>
                    </Jumbotron>
                </div>
            </Collapse>
            <br/><br/>
        </div>
    );
}

function FormGroup(props) {
    return (
        <React.Fragment>
            <Form.Group as={props.row !== undefined ? undefined: Col} >
                <Form.Label>{props.label}</Form.Label>
                <InputGroup>
                    { props.prepend !== undefined ?
                        <InputGroup.Prepend>
                            <InputGroup.Text>{props.prepend}</InputGroup.Text>
                        </InputGroup.Prepend> : null
                    }
                    { props.as === 'textarea' ?
                        <Form.Control as="textarea" rows={props.rows}
                                      style={props.disabled ? {backgroundColor: 'white'}: undefined}
                                      disabled={props.disabled}
                                      value={props.value ? props.value: undefined}
                                      onChange={props.func ? e => props.func(e.target.value) : null}
                        />
                        :
                        <Form.Control type={props.type}
                                      style={props.disabled ? {backgroundColor: 'white'}: undefined}
                                      disabled={props.disabled}
                                      placeholder={props.placeholder}
                                      value={props.value ? props.value: ''}
                                      onChange={props.func ? e => props.func(e.target.value) : null}
                        />
                    }
                </InputGroup>
            </Form.Group>
        </React.Fragment>
    );
}

function NoteLinkButton(props) {
    return (
        <MyButton
            onClick={() => {props.onClick();}}
            variant='link'
            text='>Notes'
        >
        </MyButton>
    )
}

async function savePool(poolName, description, initialFund) {
    const parsedInitialFund = parseInt(initialFund);
    if (MathUtil.isPositiveInt(parsedInitialFund)){
        const body = {poolName: poolName, description: description, initialFund: initialFund};
        await Request.POST_JSON('/exec/pool/createPool', body);
        window.location.reload(false);
    }
}

class OpenPosition {
    constructor(symbol, amount, price) {
        this.symbol = symbol;
        this.costBasis = price;
        this.amount = amount;
    }
}


export default Pool;