<script>
    import { capitalizeFirstLetter } from '../../helpers/string-helpers';
    import { template_sensor_type_color, template_sensor_type_icon } from '../../helpers/icon-helpers';
    import { roundToPrecision } from '../../helpers/number-helpers';
    import { _, time } from 'svelte-i18n';
    import { dayjs } from 'svelte-time';
    import { getCustomConfig } from '../../config';
    import { ApiUrl } from '../../constants/urls';

    let settings = getCustomConfig();
    export let enclosure = { areas: [] };
</script>

<div style="background : url({ApiUrl}/{enclosure.image}); background-size : cover">
    <div class="card-body pl-1 pr-1 dot-bg overflow-hidden" style="max-width: 100% !important">
        <table class="table table-sm text-nowrap">
            <tbody>
                {#each enclosure.areas.sort((a, b) => a.name.localeCompare(b.name)) as area}
                    <tr>
                        <td colspan="2">
                            <i
                                title="{capitalizeFirstLetter((area.setup.main_lights ? 'main ' : '') + area.type)}"
                                class="mr-1 fas {template_sensor_type_icon(
                                    (area.setup.main_lights ? 'main ' : '') + area.type
                                )} {template_sensor_type_color((area.setup.main_lights ? 'main ' : '') + area.type)}"
                                class:text-secondary="{area.mode === 'disabled'}">
                            </i>
                            {area.name}
                            <small class="text-muted ml-2 mr-2"
                                >{$_('enclosures.area.mode.title', { default: 'mode' })}: {$_(`enclosures.area.mode.${area.mode}`, {
                                    default: area.mode,
                                })}</small>
                        </td>
                        <td>
                            {#if area.mode === 'sensors'}
                                <small
                                    class="badge mt-1"
                                    class:badge-success="{area.state.powered === true}"
                                    class:badge-secondary="{area.state.powered === false}"
                                    title="{$_('enclosures.area.current_status', { default: 'Current status' })}">&nbsp;&nbsp;</small>
                            {/if}
                        </td>
                    </tr>
                    {#each ['day', 'night', 'low', 'high'] as period}
                        {#if area.state[period] && area.state[period].begin}
                            <tr>
                                <td>{$_(`enclosures.area.period.${period}`, { default: period })}:</td>
                                <td>
                                    {$time(new Date(area.state[period].begin * 1000), { format: 'medium' })} -
                                    {$time(new Date(area.state[period].end * 1000), { format: 'medium' })}
                                    ({dayjs.duration(area.state[period].duration * 1000).humanize()})
                                </td>
                                <td>
                                    <small
                                        class="badge mt-1"
                                        class:badge-success="{area.state[period].powered === true}"
                                        class:badge-secondary="{area.state[period].powered === false}"
                                        title="{$_('enclosures.area.current_status', { default: 'Current status' })}">&nbsp;&nbsp;</small>
                                </td>
                            </tr>
                        {/if}
                    {/each}
                    {#if area.state.sensors}
                        <tr>
                            <td>{$_('enclosures.area.current', { default: 'current' })}:</td>
                            <td>
                                {roundToPrecision(area.state.sensors.current)}
                                {settings.units[area.type].value} ({roundToPrecision(area.state.sensors.alarm_min)}
                                {settings.units[area.type].value} - {roundToPrecision(area.state.sensors.alarm_max)}
                                {settings.units[area.type].value})
                            </td>
                            <td>
                                {#if area.state.sensors.alarm}
                                    <i
                                        class="fas fa-exclamation-triangle text-secondary mt-1"
                                        class:text-danger="{(area.state.sensors?.alarm_low && area.setup.low.relays.length > 0) ||
                                            (area.state.sensors?.alarm_high && area.setup.high.relays.length > 0)}">
                                    </i>
                                {/if}
                            </td>
                        </tr>
                    {/if}
                {/each}
            </tbody>
        </table>
    </div>
</div>

<style>
    table.table-sm td:last-child {
        width: 1.5rem;
        position: absolute;
        right: 0px;
        margin-right: 1.25rem;
    }
</style>
